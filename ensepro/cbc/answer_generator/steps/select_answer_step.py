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
from ensepro.elasticsearch import connection
from ensepro.elasticsearch.queries import Query, QueryMultiTermSearch
from ensepro.elasticsearch.searches import execute_search
from ensepro.servicos import word_embedding as wb

remover_variaveis = configuracoes.get_config(ConsultaConstantes.REMOVER_RESULTADOS)
threshold_predicate = configuracoes.get_config(ConsultaConstantes.THRESHOLD_PREDICATE)
threshold_answer = configuracoes.get_config(ConsultaConstantes.THRESHOLD_ANSWER)
logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_SELECTING_ANSWER_STEP)


def get_resource(resource_id):
    return helper.map_var_to_resource.get(str(resource_id))


def search_in_elasticsearch(triple):
    subject = get_resource(triple[0])
    predicate = get_resource(triple[1])
    object = get_resource(triple[2])

    queryMultiTerm = QueryMultiTermSearch()
    queryMultiTerm.add_term_search(Field.FULL_MATCH_SUJEITO, subject)
    queryMultiTerm.add_term_search(Field.FULL_MATCH_PREDICADO, predicate)
    queryMultiTerm.add_term_search(Field.FULL_MATCH_OBJETO, object)

    query = Query.build_default(queryMultiTerm.build_query())

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
            else:
                tr = "p" + tr
                score += 0.5

            triple_pattern += tr

    logger.debug("Obtendo o padrão para tripla [%s] -> %s (%s)", answer["triples"], triple_pattern, str(score))
    return {
        "pattern": triple_pattern,
        "score": score
    }


def create_id_for_each_answer(previous_result):
    for index in range(len(previous_result["answers"])):
        previous_result["answers"][index]["id"] = index

    return previous_result


def find_best_pattern(previous_result):
    answers = previous_result["answers"]
    if not answers:
        return previous_result

    best_score = previous_result["answers"][0]["score"]

    best_answers_patterns = [answer_pattern_for(answer) for answer in answers if answer["score"] == best_score]

    best_answers_patterns.sort(key=lambda x: x["score"])

    previous_result["best_pattern"] = best_answers_patterns[0]

    return previous_result


def keep_only_best_pattern(previous_result):
    answers = previous_result["answers"]
    if not answers:
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
    position = ["all_subject_binded", "all_predicate_binded", "all_object_binded"]
    bind_control = {
        position[0]: True,
        position[1]: True,
        position[2]: True,
        "binds": {}
    }

    for triple in answer["triples"]:
        for index in range(len(triple)):
            resource_id = str(triple[index])
            resource = get_resource(resource_id)
            tr = helper.map_resource_to_tr.get(resource)

            if not tr:
                bind_control[position[index]] = False
                continue

            bind_control["binds"][tr["termo"]] = resource_id

    return bind_control


def create_binding_control(previous_result):
    for index in range(len(previous_result["answers"])):
        bind_control = bind_existend_values(previous_result["answers"][index])
        previous_result["answers"][index]["bind_control"] = bind_control

    return previous_result


def inject_tr_from_phrase_type(previous_result):
    # TODO needs to be done

    return previous_result


def bind_tr_to_resources(previous_result):
    trs = [tr.palavra_original for tr in helper.frase.termos_relevantes]
    for index in range(len(previous_result["answers"])):
        answer = previous_result["answers"][index]
        best_bind = {
            "score": 0,
            "resource_id": None
        }
        for triple in answer["triples"]:
            if str(triple[1]) in answer["bind_control"]["binds"]:
                continue

            original_triple = search_in_elasticsearch(triple)
            if original_triple["hits"]["total"] == 0:
                continue
            original_triple = original_triple["hits"]["hits"][0]["_source"]
            predicado = original_triple["predicado"]

            words = get_words_from_conceito(predicado["conceito"])

            for tr in trs:
                for word in words:
                    score = wb.word_embedding(tr, word)
                    if score > best_bind["score"]:
                        best_bind = {
                            "score": score,
                            "resource_id": triple[1],
                            "tr": tr
                        }

        if best_bind["score"] > threshold_predicate:
            previous_result["answers"][index]["bind_control"]["binds"][str(best_bind["resource_id"])] = best_bind["tr"]

    return previous_result


def format_concept(conecpt: str):
    return re.split(" |_", conecpt)


def validate_binded_values(previous_result):
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

        score = wb.n_word_embedding(palavras1=trs, palavras2=resources)

        logger.info("n_similarity = [%s] + [%s] = %s", str(trs), str(resources), str(score))
        if score >= threshold_answer:
            final_aswers.append(answer)

    previous_result["answers"] = final_aswers
    return previous_result


methods = [
    create_id_for_each_answer,
    find_best_pattern,
    keep_only_best_pattern,
    create_binding_control,
    inject_tr_from_phrase_type,
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

    values = {"answers": params["answers"]}
    all_answers = list(params["answers"])

    for method in methods:
        logger.debug("Executando metodo: %s", method.__name__)
        values = method(values)
        logger.debug("resultado do metodo '%s': %s", method.__name__, values)

    format_answers(values["answers"])
    format_answers(all_answers)

    return {
        "correct_answer": values["answers"],
        "all_answers": all_answers
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
