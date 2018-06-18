# -*- coding: utf-8 -*-
"""
@project ensepro
@since 07/06/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from ensepro import save_as_json
import json
from ensepro.consulta.v2 import helper
from ensepro.utils.string_utils import remover_acentos


def normalizar_value_step(params, step, steps, log=False):
    if log:
        print("normalizando resultados... ", end="")
    helper.init_helper(params["helper"])

    triplas = {}
    result_normalized = []
    result = params["result"]

    for field, value in result.items():
        for result_tripla in value["hits"]["hits"]:
            sujeito = remover_acentos(result_tripla["_source"]["sujeito"]["conceito"])
            predicado = remover_acentos(result_tripla["_source"]["predicado"]["conceito"])
            objeto = remover_acentos(result_tripla["_source"]["objeto"]["conceito"])

            tripla = [sujeito, predicado, objeto]

            tripla_ja_existe = triplas.get(tripla[0] + "-" + tripla[1] + "-" + tripla[2], None)

            if not tripla_ja_existe:
                triplas[tripla[0] + "-" + tripla[1] + "-" + tripla[2]] = tripla
                alterar_para_variaveis(tripla)
                result_normalized.append(tripla)

    if log:
        print("done -> size=", len(result_normalized))
    helper_values = helper.save_helper()

    if steps.get(step, None):
        values = {}
        values["values"] = result_normalized
        values["helper"] = helper_values
        save_as_json(values, "resultado_normalizado.json")
        return steps[step][0](values, steps[step][1], steps, log=log)
    else:
        return result_normalized


def normalizar_step(params, step, steps, log=False):
    with open(params[0], encoding="UTF-8", mode="r") as f:
        value = json.load(f)

    return normalizar_value_step(value, step, steps, log=log)


# 3. Remover todas os valores que não são TR, passando estes para um dicionário -> { variável : TR }
def alterar_para_variaveis(tripla):
    for index in range(len(tripla)):
        tr = helper._termo_relevante_from_resource(tripla[index])
        if tr:
            tripla[index] = tr
        else:
            tripla[index] = helper._get_var_name(tripla[index])
