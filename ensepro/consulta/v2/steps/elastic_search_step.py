# -*- coding: utf-8 -*-
"""
@project ensepro
@since 07/06/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from ensepro.consulta.fields import Field
from ensepro.elasticsearch.searches import list_parcial_match_search
from ensepro.utils.string_utils import remover_acentos
from ensepro import save_as_json
from ensepro.consulta.v2 import helper

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
