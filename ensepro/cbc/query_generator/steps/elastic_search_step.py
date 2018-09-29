# -*- coding: utf-8 -*-
"""
@project ensepro
@since 07/06/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from ensepro.cbc.fields import Field
from ensepro.elasticsearch.searches import list_parcial_match_search
from ensepro.utils.string_utils import remover_acentos
from ensepro import save_as_json
from ensepro.cbc.query_generator import helper

fields_partial_match = [
    Field.PARTIAL_MATCH_SUJEITO,
    Field.PARTIAL_MATCH_PREDICADO,
    Field.PARTIAL_MATCH_OBJETO
]


def elastic_search_step(params, step, steps, log=False):
    obtem_termos_relevantes(params)

    if not helper.termos_relevantes:
        if log:
            print("Nenhum termo relevante indicado.")
        exit(1)

    tr = [t[0] for t in helper.termos_relevantes]
    # 1. Search in elasticsearch todos as triplas que contém algum TR
    if log:
        print("consultando triplas... ", end="")
    result = list_parcial_match_search(fields_partial_match, tr)
    if result["keys"]:
        if log:
            print("done.")
        if steps.get(step, None):
            result["helper"] = helper.save_helper()
            save_as_json(result, "elastic_search_step.json")
            return steps[step][0](result, steps[step][1], steps, log=log)
        else:
            return result

    raise Exception("Nenhuma tripla encontrada para termos relevantes: ", tr)


def elastic_search_integrado_step(params, step, steps, log=False):
    integrado_obtem_termos_relevantes(params["termos"])

    if not helper.termos_relevantes:
        if log:
            print("Nenhum termo relevante indicado.")
        exit(1)

    termos_relecionados(params["frase"])

    busca_parte1 = list_parcial_match_search(
            [
                Field.PARTIAL_MATCH_SUJEITO,
                Field.PARTIAL_MATCH_OBJETO
            ],
            params["termos"]["substantivos_proprios"][::2]
    )

    busca_parte2 = list_parcial_match_search(
            [
                Field.PARTIAL_MATCH_SUJEITO,
                Field.PARTIAL_MATCH_PREDICADO,
                Field.PARTIAL_MATCH_OBJETO
            ],
            params["termos"]["substantivos_comuns"][::2]
    )

    busca_parte3 = list_parcial_match_search(
            [
                Field.PARTIAL_MATCH_PREDICADO
            ],
            params["termos"]["verbos"][::2]

    )
    resultado = {}
    resultado["result"] = merge_consultas([busca_parte1, busca_parte2, busca_parte3])

    if resultado.get("result", None):
        if log:
            print("done.")
        if steps.get(step, None):
            resultado["helper"] = helper.save_helper()
            save_as_json(resultado, "elastic_search_step.json")
            return steps[step][0](resultado, steps[step][1], steps, log=log)
        else:
            return resultado


def termos_relecionados(frase):
    for tr in frase.termos_relevantes:
        termo_principal = remover_acentos(tr.palavra_canonica).lower()

        if tr.is_substantivo_proprio():
            helper.substantivos_proprios_frase.append(termo_principal)

        helper.termos_relacionados[termo_principal] = []
        helper.sinonimos[termo_principal] = termo_principal
        for key, sinonimos in tr.sinonimos.items():
            for sinonimo in sinonimos:
                sinonimo = remover_acentos(sinonimo.sinonimo).lower()
                helper.termos_relacionados[termo_principal].append(sinonimo)
                helper.sinonimos[sinonimo] = termo_principal


        for sin in helper.termos_relacionados[termo_principal]:
            sinonimos_temp = helper.termos_relacionados[termo_principal].copy()
            sinonimos_temp.remove(sin)
            sinonimos_temp.append(termo_principal)
            helper.termos_relacionados[sin] = sinonimos_temp


def merge_consultas(values):
    i = 0
    resultado = {}
    for value in values:
        if value["keys"]:
            result = value["result"]
            for field, _value in result.items():
                _field = field
                while (_field in resultado):
                    i += 1
                    _field += str(i)

                resultado[_field] = _value

    return resultado


def integrado_obtem_termos_relevantes(params):
    for key in params:
        obtem_termos_relevantes(params[key])


def obtem_termos_relevantes(params):
    i = 0
    while (i < len(params)):
        termo = remover_acentos(params[i]).lower()
        if i + 1 < len(params):
            peso = is_int(params[i + 1])
        else:
            peso = None

        if not peso:
            peso = 1
            i += 1
        else:
            i += 2

        helper.termos_relevantes.append((termo, peso))


def is_int(s):
    try:
        return int(s)
    except ValueError:
        return None
