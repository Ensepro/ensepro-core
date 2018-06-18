# -*- coding: utf-8 -*-
"""
@project ensepro
@since 08/06/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from ensepro import save_as_json
import json
from ensepro.consulta.v2 import helper


def calcular_metricas_value(params, step, steps, log=False):
    helper.init_helper(params["helper"])
    triplas = params["values"]

    if log:
        print("calculando metricas... [", len(triplas), "]", end="")

    for t in triplas:
        calcular(t)

    if log:
        print("done")

    if steps.get(step, None):
        values = {}
        values["helper"] = helper.save_helper()
        values["values"] = triplas
        save_as_json(values, "calcular_metricas_step.json")
        return steps[step][0](values, steps[step][1], steps, log=log)
    else:
        return triplas


def calcular_metricas_step(params, step, steps, log=False):
    with open(params[0], encoding="UTF-8", mode="r") as f:
        value = json.load(f)

    return calcular_metricas_value(value, step, steps, log=log)


# 5. Fazer cálculos
def calcular(combinacao):
    var_count = 0
    tr_elements = set()
    some_distancias = 0
    for tripla in combinacao:
        for resource_var_name in tripla:
            tr = helper._termo_relevante_from_var(resource_var_name)
            if tr:
                some_distancias += helper._calcular_distancia_edicao(tr[0], resource_var_name)
                tr_elements.add((tr[0], tr[1]))
            else:
                var_count += 1

    calc_tr = 0
    for t in tr_elements:
        calc_tr += t[1]

    combinacao.append(int(var_count))
    combinacao.append(int(calc_tr))
    combinacao.append(int(some_distancias))
