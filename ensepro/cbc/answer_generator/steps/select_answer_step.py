# -*- coding: utf-8 -*-
"""
@project ensepro
@since 08/06/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import json
import re

import ensepro.configuracoes as configuracoes
from ensepro import ConsultaConstantes, LoggerConstantes
from ensepro.cbc.answer_generator import helper
from ensepro.cbc.fields import Field
from ensepro.classes.classe_gramatical import ClasseGramatical
from ensepro.cln import nominalizacao
from ensepro.elasticsearch import connection
from ensepro.elasticsearch.queries import Query, QueryMultiTermSearch
from ensepro.elasticsearch.searches import execute_search
from ensepro.servicos import word_embedding as wb
from ensepro.utils.string_utils import remover_acentos

remover_variaveis = configuracoes.get_config(ConsultaConstantes.REMOVER_RESULTADOS)
threshold_predicate = configuracoes.get_config(ConsultaConstantes.THRESHOLD_PREDICATE)
threshold_answer = configuracoes.get_config(ConsultaConstantes.THRESHOLD_ANSWER)

numero_respostas = configuracoes.get_config(ConsultaConstantes.NUMERO_RESPOSTAS)

termos_tipos_frases = configuracoes.get_config(ConsultaConstantes.TERMOS_TIPOS_FRASES)

logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_SELECTING_ANSWER_STEP)


def get_resource(resource_id):
    return helper.map_var_to_resource.get(str(resource_id))


def search_in_elasticsearch(triple):
    subject = get_resource(triple[0])
    predicate = get_resource(triple[1])
    object = get_resource(triple[2])

    query_multi_term = QueryMultiTermSearch()
    query_multi_term.add_term_search(Field.FULL_MATCH_SUJEITO, subject)
    query_multi_term.add_term_search(Field.FULL_MATCH_PREDICADO, predicate)
    query_multi_term.add_term_search(Field.FULL_MATCH_OBJETO, object)

    query = Query.build_default(query_multi_term.build_query())

    return execute_search(connection(), query)


def get_words_from_conceito(word):
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', word)
    return [m.group(0) for m in matches]


def answer_pattern_for(answer, reversed_=False):
    """
    TODO
    for each fullmatch, add 1.1
    for each partialmatch add 0.5
    """

    triple_pattern = ""
    score = 0.0
    full_match_count = 0
    triples = answer["triples"] if not reversed_ else answer["triples"][::-1]
    for triple in triples:
        for value in triple:
            resource = get_resource(value)
            tr = helper.map_resource_to_tr.get(resource)
            if not tr:
                continue

            tr = tr["termo"]
            if tr not in answer["detail"]["keywords"]:
                continue

            if resource == tr:
                tr = "f" + tr
                score += 1.1
                full_match_count += 1
            else:
                tr = "p" + tr
                score += 0.5

            triple_pattern += tr

    logger.debug("Obtendo o padrão para tripla [%s] -> %s (%s)", answer["triples"], triple_pattern, str(score))
    return {
        "pattern": triple_pattern,
        "score": score,
        "full_match_count": full_match_count
    }


def create_id_for_each_answer(previous_result):
    for index in range(len(previous_result["answers"])):
        previous_result["answers"][index]["id"] = index

    return previous_result


def validate_answer_0(previous_result):
    answer_0 = previous_result["answers"][0]

    if answer_0["detail"]["proper_nouns_count"] > answer_0["detail"]["proper_nouns_matched_count"]:
        previous_result["answers"] = []
        previous_result["continue"] = False

    return previous_result


def find_best_pattern(previous_result):
    answers = previous_result["answers"]
    if not answers:
        previous_result["continue"] = False
        return previous_result

    best_score = previous_result["answers"][0]["score"]

    best_answers_patterns = [answer_pattern_for(answer) for answer in answers if answer["score"] == best_score]

    best_answers_patterns.sort(key=lambda x: x["score"])

    previous_result["best_pattern"] = best_answers_patterns[0]

    return previous_result


def keep_only_best_pattern(previous_result):
    answers = previous_result["answers"]
    if not answers:
        previous_result["continue"] = False
        return previous_result

    answer_same_pattern = []

    for answer in answers:
        answer_pattern = answer_pattern_for(answer)

        if answer_pattern["pattern"] == previous_result["best_pattern"]["pattern"]:
            answer_same_pattern.append(answer)
            continue

        if len(answer["triples"]) > 1:
            answer_pattern = answer_pattern_for(answer, reversed_=True)
            if answer_pattern["pattern"] == previous_result["best_pattern"]:
                continue

        if answers[0]["score"] != answer["score"]:
            break

    previous_result["answers"] = answer_same_pattern

    return previous_result


def bind_existend_values(answer):
    bind_control = {
        "binds": {},
        "best_bind": {"score": 0}
    }

    for triple in answer["triples"]:
        for index in range(len(triple)):
            resource_id = str(triple[index])
            resource = get_resource(resource_id)
            tr = helper.map_resource_to_tr.get(resource)

            if not tr:
                continue

            if tr["termo"] in bind_control["binds"]:
                continue

            bind_control["binds"][tr["termo"]] = resource_id

    return bind_control


def create_binding_control(previous_result):
    for index in range(len(previous_result["answers"])):
        bind_control = bind_existend_values(previous_result["answers"][index])
        previous_result["answers"][index]["bind_control"] = bind_control

    return previous_result


def select_tr_to_bind(previous_result):
    trs = [remover_acentos(tr.palavra_canonica.lower()) for tr in helper.frase.termos_relevantes]

    if len(helper.frase.termos_relevantes) == 1:
        trs_to_inject = termos_tipos_frases.get(helper.frase.tipo.tipo, [])
        logger.info("Frase com somente 1 TR: Injetando TRs: %s", str(trs_to_inject))
        trs += trs_to_inject

    previous_result["trs"] = trs
    return previous_result


def bind_tr_to_resources(previous_result):
    answers = previous_result["answers"]
    if not answers:
        logger.debug("Sem respostas, retornando.")
        previous_result["continue"] = False
        return previous_result

    if len(answers) == 1:
        logger.debug("Somente 1 resposta, ignorando esta etapa")
        return previous_result

    subject = answers[0]["triples"][0][0]  # subject of the first triple of the first answer
    predicate = answers[0]["triples"][0][1]  # predicate of the first triple of the first answer
    _object = answers[0]["triples"][0][2]  # object of the first triple of the first answer
    all_same_subject = True
    all_same_predicate = True
    all_same_object = True
    for answer in answers:
        for triple in answer["triples"]:
            all_same_subject = triple[0] == subject and all_same_subject
            all_same_predicate = triple[1] == predicate and all_same_predicate
            all_same_object = triple[2] == _object and all_same_object
            if not all_same_predicate:
                break

    if all_same_predicate:
        previous_result["continue"] = not (all_same_subject or all_same_object)
        return previous_result

    verbs = [tr.palavra_canonica for tr in helper.frase.termos_relevantes if
             tr.classe_gramatical == ClasseGramatical.VERBO]

    map_nominalizacoes = {}
    for verb in verbs:
        map_nominalizacoes[verb] = nominalizacao.get(verb)

    trs = previous_result["trs"]
    for index in range(len(previous_result["answers"])):
        answer = previous_result["answers"][index]
        predicates_looked = []
        for triple in answer["triples"]:
            if str(triple[1]) in predicates_looked:
                continue

            predicates_looked.append(str(triple[1]))

            original_triple = search_in_elasticsearch(triple)
            if original_triple["hits"]["total"] == 0:
                continue
            original_triple = original_triple["hits"]["hits"][0]["_source"]
            predicado = original_triple["predicado"]

            words = get_words_from_conceito(predicado["conceito"])

            for tr in trs:
                if tr in answer["bind_control"]["binds"]:
                    continue
                tr_with_nominalization = [tr]
                nominalizacoes = map_nominalizacoes.get(tr, [])
                if nominalizacoes:
                    tr_with_nominalization += nominalizacoes

                for val in tr_with_nominalization:
                    score = 0
                    for word in words:
                        score += wb.word_embedding(val, word)

                    avg_score = score / len(words)
                    logger.debug("Similaridade média: [%s + %s] = %s", val, predicado["conceito"], avg_score)

                    if avg_score > answer["bind_control"]["best_bind"]["score"]:
                        answer["bind_control"]["best_bind"] = {
                            "score": avg_score,
                            "resource_id": triple[1],
                            "tr": tr
                        }

        best_bind = answer["bind_control"]["best_bind"]
        if best_bind["score"] >= threshold_predicate:
            previous_result["answers"][index]["bind_control"]["binds"][str(best_bind["tr"])] = best_bind["resource_id"]

    previous_result["answers"].sort(key=lambda x: x["bind_control"]["best_bind"]["score"], reverse=True)

    matches_count = len(previous_result["answers"][0]["bind_control"]["binds"])
    score = previous_result["answers"][0]["bind_control"]["best_bind"]["score"]

    previous_result["answers"] = [answer for answer in previous_result["answers"]
                                  if len(answer["bind_control"]["binds"]) == matches_count
                                  and answer["bind_control"]["best_bind"]["score"] == score
                                  and answer["bind_control"]["best_bind"]["score"] >= threshold_predicate]

    return previous_result


def format_concept(conecpt: str):
    return re.split(" |_", conecpt)


def validate_binded_values(previous_result):
    
    _continue = False
    for answer in previous_result["answers"]:
        if answer_pattern_for(answer)["full_match_count"] < 2
            _continue = True
            break
            
    if not _continue:
        logger.info("Todas respostas com 2 ou mais fullmatches, ignorando validação.")
        return previous_result
                
    trs = []
    final_aswers = []
    for tr in helper.frase.termos_relevantes:
        trs += format_concept(tr.palavra_original.lower())

    for answer in previous_result["answers"]:
        resources = []
        for triple in answer["triples"]:
            original_triple = search_in_elasticsearch(triple)
            if original_triple["hits"]["total"] == 0:
                continue
            original_triple = original_triple["hits"]["hits"][0]["_source"]

            subject = original_triple["sujeito"]
            predicado = original_triple["predicado"]
            object = original_triple["objeto"]

            words_sub = get_words_from_conceito(subject["conceito"])
            words_pred = get_words_from_conceito(predicado["conceito"])
            words_obj = get_words_from_conceito(object["conceito"])

            for word in words_sub:
                resources += format_concept(word.lower())

            for word in words_pred:
                resources += format_concept(word.lower())

            for word in words_obj:
                resources += format_concept(word.lower())

        result = wb.n_word_embedding(palavras1=list(set(trs)), palavras2=list(set(resources)))
        score = result["score"]

        logger.info("n_similarity = [%s] + [%s] = %s", result["words1"], result["words2"], str(score))
        if score >= threshold_answer:
            final_aswers.append(answer)

    previous_result["answers"] = final_aswers
    return previous_result


methods = [
    create_id_for_each_answer,
    validate_answer_0,
    find_best_pattern,
    keep_only_best_pattern,
    create_binding_control,
    select_tr_to_bind,
    bind_tr_to_resources,
    validate_binded_values
]


def select_answer_value(params, step, steps, log=False):
    logger.info("Iniciando selecting_answer_step")
    helper.init_helper(params["helper"])
    helper.frase = params["frase"]

    logger.info("Resultado java: size=%s", len(params["answers"]))
    if not remover_variaveis:
        return params["answers"]

    values = {"answers": params["answers"], "continue": True}
    all_answers = list(params["answers"])

    for method in methods:
        logger.debug("Executando metodo: %s", method.__name__)
        values = method(values)
        # logger.debug("resultado do metodo '%s': %s", method.__name__, values)
        if not values["continue"]:
            break

    format_answers(values["answers"])
    format_answers(all_answers)

    return {
        "correct_answer": values["answers"],
        "all_answers": all_answers[:numero_respostas]
    }


def select_answer_step(params, step, steps, log=False):
    with open(params[0], encoding="UTF-8", mode="r") as f:
        value = json.load(f)
    value["frase"] = params[2]
    return select_answer_value(value, step, steps, log=log)


def format_answers(best_answers):
    for value in best_answers:
        for tripla in value["triples"]:
            for index in range(0, len(tripla)):
                var = str(tripla[index])
                value_temp = helper._get_var_value(var)
                if value_temp:
                    try:
                        if tripla[index] < 0:
                            value_temp = "*" + value_temp
                        tripla[index] = value_temp
                    except:
                        pass
