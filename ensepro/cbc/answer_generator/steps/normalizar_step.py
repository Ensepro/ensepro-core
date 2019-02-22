# -*- coding: utf-8 -*-
"""
@project ensepro
@since 07/06/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from ensepro import save_as_json, LoggerConstantes
import json
from ensepro.cbc.answer_generator import helper
from ensepro.utils.string_utils import remover_acentos
from ensepro import ConsultaConstantes, LoggerConstantes
import ensepro.configuracoes as configuracoes

logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_NORMALIZAR_STEP)
nivel = configuracoes.get_config(ConsultaConstantes.NIVEL_ANSWER_GENERATOR)


def normalizar_value_step(params, step, steps):
    logger.debug("normalizando resultados... ")
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

    logger.info("done -> size=%s", len(result_normalized))
    helper_values = helper.save_helper()

    if steps.get(step, None):
        values = {}
        values["values"] = result_normalized
        values["helper"] = helper_values
        values["nivel_combination"] = get_nivel(params["frase"], nivel)
        values["frase"] = params["frase"]
        save_as_json(values, "resultado_normalizado.json")
        return steps[step][0](values, steps[step][1], steps)
    else:
        return result_normalized


def normalizar_step(params, step, steps):
    with open(params[0], encoding="UTF-8", mode="r") as f:
        value = json.load(f)

    return normalizar_value_step(value, step, steps)


# 3. Remover todas os valores que não são TR, passando estes para um dicionário -> { variável : TR }
def alterar_para_variaveis(tripla):
    for index in range(len(tripla)):
        tr = helper._termo_relevante_from_resource(tripla[index])
        if tr:
            tripla[index] = tr
        else:
            tripla[index] = helper._get_var_name(tripla[index])


def get_nivel(frase, nivel_default):
    if not frase:
        return nivel_default

    if len(frase.termos_relevantes) > 2:
        return nivel_default

    tem_prop = False
    for tr in frase.termos_relevantes:
        tem_prop = tem_prop or tr.is_substantivo_proprio()

        if "<KOMP>" in tr.tags:
            return nivel_default
        if "<NUM-ord>" in tr.tags:
            return nivel_default

    return 1 if tem_prop else nivel_default
