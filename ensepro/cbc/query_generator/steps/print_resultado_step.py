# -*- coding: utf-8 -*-
"""
@project ensepro
@since 08/06/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import json
from ensepro import save_as_json
from ensepro.cbc.query_generator import helper
import ensepro.configuracoes as configuracoes
from ensepro import ConsultaConstantes

numero_respostas = configuracoes.get_config(ConsultaConstantes.NUMERO_RESPOSTAS)


def print_resultado_value(params, step, steps, log=False):
    helper.init_helper(params["helper"])

    if log:
        print("\n\nExibindo os 20 melhores resultados para:", helper.termos_relevantes)
    values_to_print = params["values"][:numero_respostas]

    v = set()
    print()
    for value in values_to_print:
        for tripla in value:
            if type(tripla) is list:
                for index in range(len(tripla)):
                    if tripla[index][0] == "z":
                        tripla[index] = "*" + helper._get_var_value(tripla[index])
                    elif tripla[index][0] == "x":
                        if log:
                            v.add(tripla[index])
                        else:
                            tripla[index] = helper._get_var_value(tripla[index])

        if log:
            print(value)

    vars_values = []
    if log:
        for v1 in v:
            var_value = helper._get_var_value(v1)
            print(v1, "=", var_value)
            vars_values.append((v1, var_value))

    if steps.get(step, None):
        values = {}
        values["values"] = values_to_print
        values["vars"] = vars_values
        values["helper"] = helper.save_helper()
        save_as_json(values, "melhores_resultados.json")
        return steps[step][0](values, steps[step][1], steps, log=log)
    else:
        return values_to_print


def print_resultado(params, step, steps, log=False):
    with open(params[0], encoding="UTF-8", mode="r") as f:
        value = json.load(f)

    return print_resultado_value(value, step, steps, log=log)
