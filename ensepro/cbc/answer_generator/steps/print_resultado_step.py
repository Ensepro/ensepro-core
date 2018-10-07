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


def print_resultado_value(params, step, steps, log=False):
    helper.init_helper(params["helper"])

    if log:
        print("\n\nExibindo os 20 melhores resultados para:", helper.termos_relevantes)
    values_to_print = params["answers"]

    if not remover_variaveis:
        return values_to_print

    for value in values_to_print:
        for tripla in value["triples"]:
            for key in tripla:
                value_temp = helper._get_var_value(tripla[key])
                if tripla[key][0] == "z":
                    value_temp = "*" + value_temp
                tripla[key] = value_temp

    return values_to_print


def print_resultado(params, step, steps, log=False):
    with open(params[0], encoding="UTF-8", mode="r") as f:
        value = json.load(f)

    return print_resultado_value(value, step, steps, log=log)
