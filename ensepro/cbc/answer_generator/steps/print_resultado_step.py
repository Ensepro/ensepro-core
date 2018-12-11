# -*- coding: utf-8 -*-
"""
@project ensepro
@since 08/06/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import json
from ensepro.cbc.answer_generator import helper
import ensepro.configuracoes as configuracoes
from ensepro import ConsultaConstantes

remover_variaveis = configuracoes.get_config(ConsultaConstantes.REMOVER_RESULTADOS)

answer_doesnt_exist_respose = {}


def analise_nivel_1_1(values):
    # verifica se a resposta 0 possui todos os TRs PROPs

    tr_prop_existe = [tr for tr in helper.termos_relevantes if tr[2] == "PROP"]
    answer_0 = values["answers"][0]
    count_props = 0

    for keyword in answer_0["details"]["weightClasses"]["keyword"]:
        if keyword["grammarClass"] == "PROP":
            count_props += 1

    if count_props != len(tr_prop_existe):
        return {
            "answer_found": False,
            "continue": False
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
                triple_pattern += str(value)
    return triple_pattern


def analise_nivel_1_2(values):
    # obtem as demais triplas com o mesmo padrao
    # se existir somente 1 padrao igual, retorna que encontrou a resposta

    answer_0_pattern = values["answer_0_pattern"]
    answer_match_answer_0_pattern = []

    for answer in values["answers"]:
        answer_pattern = get_triples_pattern(answer["triples"])
        if answer_pattern == answer_0_pattern:
            answer_match_answer_0_pattern.append(answer)

    answer_found = len(answer_match_answer_0_pattern) == 1
    should_continue = not answer_found

    return {
        "answer_found": answer_found,
        "continue": should_continue,
        "answers": answer_match_answer_0_pattern
    }


def analise_nivel_2_1(values):
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
            return {
                "answer_found": False,
                "continue": True
            }

    return {
        "answer_found": True,
        "continue": False,
        "answers": values["answers"]
    }


def analise_nivel_2_2(values):
    #
    pass


methods = [analise_nivel_1_1, analise_nivel_1_2, analise_nivel_2_1]


def print_resultado_value(params, step, steps, log=False):
    helper.init_helper(params["helper"])

    if log:
        print("\n\nExibindo os 20 melhores resultados para:", helper.termos_relevantes)
    answers = params["answers"]

    if not remover_variaveis:
        return answers

    values = {"answers": answers}
    answers = []
    for method in methods:
        values = method(values)
        if values["answer_found"]:
            answers = values["answers"]
        if not values["continue"]:
            break

    format_answers(answers)

    return answers


def format_answers(best_answers):
    for value in best_answers:
        for tripla in value["triples"]:
            for key in tripla:
                value_temp = helper._get_var_value(str(tripla[key]))
                if tripla[key] < 0:
                    value_temp = "*" + value_temp
                tripla[key] = value_temp


def print_resultado(params, step, steps, log=False):
    with open(params[0], encoding="UTF-8", mode="r") as f:
        value = json.load(f)

    return print_resultado_value(value, step, steps, log=log)
