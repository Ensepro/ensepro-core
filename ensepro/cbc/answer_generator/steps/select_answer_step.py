# -*- coding: utf-8 -*-
"""
@project ensepro
@since 08/06/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import json
import re
import time
import copy
from ensepro.cbc.answer_generator import helper
import ensepro.configuracoes as configuracoes
from ensepro import ConsultaConstantes, LoggerConstantes
from ensepro.cbc.fields import Field
from ensepro.elasticsearch import connection
from ensepro.elasticsearch.searches import execute_search
from ensepro.elasticsearch.queries import Query, QueryMultiTermSearch

remover_variaveis = configuracoes.get_config(ConsultaConstantes.REMOVER_RESULTADOS)

logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_SELECTING_ANSWER_STEP)

answer_doesnt_exist_respose = {}


def answer_0_correct(values):
    # verifica se a resposta 0 possui todos os TRs PROPs

    answer_0 = values["answers"][0]
    count_tr_prop_existe = len([tr for tr in helper.termos_relevantes if tr[2] == "PROP"])
    count_answer_0_prop = answer_0["details"]["nounsMatch"]

    if count_answer_0_prop != count_tr_prop_existe:
        logger.info("Resposta 0 não possui todos os tr_prop")
        return {
            "answer_found": False,
            "continue": False,
        }

    answer_0_pattern = get_triples_pattern(answer_0["triples"])

    return {
        "answer_found": False,
        "continue": True,
        "answers": values["answers"],
        "answer_0_pattern": answer_0_pattern
    }


def get_triples_pattern(triples):
    triple_pattern = ""
    for triple in triples:
        for value in triple.values():
            if value < 0:
                triple_pattern += helper.map_resource_to_tr.get(helper.map_var_to_resource.get(str(value)))[0]
    logger.debug("Obtendo o padrão para tripla [%s] -> %s", triples, triple_pattern)
    return triple_pattern


def get_answers_with_same_pattern(values):
    # obtem as demais triplas com o mesmo padrao
    # se existir somente 1 padrao igual, retorna que encontrou a resposta

    answer_0_pattern = values["answer_0_pattern"]
    answer_match_answer_0_pattern = []

    answer_0 = values["answers"][0]

    for answer in values["answers"]:
        answer_pattern = get_triples_pattern(answer["triples"])
        if answer_pattern == answer_0_pattern:
            answer_match_answer_0_pattern.append(answer)
            continue

        if len(answer["triples"]) > 1:
            answer_pattern = get_triples_pattern(answer["triples"][::-1])
            if answer_pattern == answer_0_pattern:
                continue

        if answer_0["score"] != answer["score"]:
            break

    answer_found = len(answer_match_answer_0_pattern) == 1
    should_continue = not answer_found

    return {
        "answer_found": answer_found,
        "continue": should_continue,
        "answers": answer_match_answer_0_pattern
    }


def answers_have_same_predicate(values):
    # verifica se todas os PREDICATE são iguais, se sim, todas são respostas
    answers = values["answers"]
    for index, current_answer in enumerate(answers):
        if index == len(answers) - 1:
            # the last time cannot be done because its doing index+1
            break
        next_answer = answers[index + 1]

        current_triple_predicates_pattern = ""
        next_triple_predicates_pattern = ""

        for triple in current_answer["triples"]:
            current_triple_predicates_pattern += str(triple["predicate"])

        for triple in next_answer["triples"]:
            next_triple_predicates_pattern += str(triple["predicate"])

        if current_triple_predicates_pattern != next_triple_predicates_pattern:
            logger.info("Quebrou o padrão das triple, ignorando demais triplas")
            return {
                "answer_found": False,
                "continue": True,
                "answers": values["answers"]
            }

    return {
        "answer_found": True,
        "continue": False,
        "answers": values["answers"]
    }


def get_resource(element):
    return helper.map_var_to_resource.get(str(element))


def search_in_elasticsearch(triple):
    subject = get_resource(triple["subject"])
    predicate = get_resource(triple["predicate"])
    object = get_resource(triple["object"])

    queryMultiTerm = QueryMultiTermSearch()
    queryMultiTerm.add_term_search(Field.FULL_MATCH_SUJEITO, subject)
    queryMultiTerm.add_term_search(Field.FULL_MATCH_PREDICADO, predicate)
    queryMultiTerm.add_term_search(Field.FULL_MATCH_OBJETO, object)

    query = Query.build_default(queryMultiTerm.build_query())

    return execute_search(connection(), query)


def get_words_from_conceito(word):
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', word)
    return [m.group(0) for m in matches]


def word_embedding(values):
    from ensepro.servicos import word_embedding as wb
    from ensepro.cln import nominalizacao
    answers = values["answers"]

    verbo = [tr[0] for tr in helper.termos_relevantes if tr[2] == "VERB"]

    if not verbo:
        logger.info("Frase não possui verbo. Ignorando execução do word_embedding")
        return {
            "answer_found": False,
            "continue": True,
            "answers": []
        }

    verbo_nominalizado = nominalizacao.get(verbo[0])

    if verbo_nominalizado:
        verbo = verbo_nominalizado[0]

    best_answer = []
    best_score = 0
    for answer in answers:
        for triple in answer["triples"]:
            original_triple = search_in_elasticsearch(triple)
            if original_triple["hits"]["total"] == 0:
                continue
            original_triple = original_triple["hits"]["hits"][0]["_source"]
            # sujeito = original_triple["sujeito"]
            predicado = original_triple["predicado"]
            # objeto = original_triple["objeto"]

            words = get_words_from_conceito(predicado["conceito"])
            score = 0
            for word in words:
                temp_score = wb.word_embedding(verbo, word)
                if temp_score > score:
                    score = temp_score
                # if word_embedding_result["related"]:
                #     if word_embedding_result["related"][0]["weight"] > score:
                #         score = word_embedding_result["related"][0]["weight"]

            # print(sujeito["conceito"], predicado["conceito"], objeto["conceito"])
            if score > best_score:
                best_answer.clear()
                best_score = score
            if score == best_score:
                best_answer.append(copy.deepcopy(answer))

    return {
        "answer_found": True,
        "continue": False,
        "answers": best_answer
    }


methods = [answer_0_correct, get_answers_with_same_pattern, answers_have_same_predicate, word_embedding]


def select_answer_value(params, step, steps, log=False):
    logger.info("Iniciando selecting_answer_step")
    helper.init_helper(params["helper"])
    frase = params["frase"]

    if log:
        print("\n\nExibindo os 20 melhores resultados para:", helper.termos_relevantes)
    answers = params["answers"]

    if not remover_variaveis:
        return answers

    values = {"answers": answers}
    all_answers = list(answers)
    answers = []
    for method in methods:
        logger.debug("Executando metodo: %s", method.__name__)
        values = method(values)
        logger.debug("resultado do metodo '%s': %s", method.__name__, values)

        if values["answer_found"]:
            answers = values["answers"]
        if not values["continue"]:
            break

    format_answers(answers)
    format_answers(all_answers)

    return {
        "correct_answer": answers,
        "all_answers": all_answers
    }


def select_answer_step(params, step, steps, log=False):
    with open(params[0], encoding="UTF-8", mode="r") as f:
        value = json.load(f)
    value["frase"] = params[1]
    return select_answer_value(value, step, steps, log=log)


def format_answers(best_answers):
    for value in best_answers:
        for tripla in value["triples"]:
            for key in tripla:
                value_temp = helper._get_var_value(str(tripla[key]))
                if value_temp:
                    if tripla[key] < 0:
                        value_temp = "*" + value_temp
                    tripla[key] = value_temp
