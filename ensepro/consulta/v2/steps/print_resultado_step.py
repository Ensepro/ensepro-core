# -*- coding: utf-8 -*-
"""
@project ensepro
@since 08/06/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import json
from ensepro import save_as_json
from ensepro.consulta.v2 import helper


def print_resultado_value(params, step, steps):
    helper.init_helper(params["helper"])

    print("\n\nExibindo os 20 melhores resultados para:", helper.termos_relevantes)
    values_to_print = params["values"][:20]

    v = set()
    print()
    for value in values_to_print:
        for tripla in value:
            if type(tripla) is list:
                for index in range(len(tripla)):
                    if tripla[index][0] == "z":
                        tripla[index] = helper._get_var_value(tripla[index])
                    elif tripla[index][0] == "x":
                        v.add(tripla[index])

        print(value)

    vars_values = []
    for v1 in v:
        var_value = helper._get_var_value(v1)
        print(v1, "=", var_value)
        vars_values.append((v1, var_value))

    values = {}
    values["values"] = values_to_print
    values["vars"] = vars_values
    values["helper"] = helper.save_helper()

    save_as_json(values, "melhores_resultados.json")
    if steps.get(step, None):
        steps[step][0](values, steps[step][1], steps)


def print_resultado(params, step, steps):
    with open(params[0], encoding="UTF-8", mode="r") as f:
        value = json.load(f)

    print_resultado_value(value, step, steps)
