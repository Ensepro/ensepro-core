# -*- coding: utf-8 -*-
"""
@project ensepro
@since 08/06/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
from ensepro.configuracoes import get_config
from ensepro import ConsultaConstantes
import editdistance
import json

map_resource_to_var = {}
map_var_to_resource = {}
map_resource_to_tr = {}
termos_relevantes = []
termos_relacionados = {}
sinonimos = {}
substantivos_proprios_frase = []
peso_m1 = get_config(ConsultaConstantes.PESO_M1)
peso_m2 = get_config(ConsultaConstantes.PESO_M2)
peso_m3 = get_config(ConsultaConstantes.PESO_M3)

var_id = 1
var_prefixes = {True: "z", False: "x"}


def init_helper(values):
    global map_resource_to_var
    global map_var_to_resource
    global map_resource_to_tr
    global termos_relevantes
    global termos_relacionados
    global sinonimos
    global substantivos_proprios_frase

    map_resource_to_var = values.get("map_resource_to_var", map_resource_to_var)
    map_var_to_resource = values.get("map_var_to_resource", map_var_to_resource)
    map_resource_to_tr = values.get("map_resource_to_tr", map_resource_to_tr)
    termos_relevantes = values.get("termos_relevantes", termos_relevantes)
    termos_relacionados = values.get("termos_relacionados", termos_relacionados)
    sinonimos = values.get("sinonimos", sinonimos)
    substantivos_proprios_frase = values.get("substantivos_proprios_frase", substantivos_proprios_frase)


def save_helper():
    helper = {}
    helper["map_resource_to_var"] = map_resource_to_var
    helper["map_var_to_resource"] = map_var_to_resource
    helper["map_resource_to_tr"] = map_resource_to_tr
    helper["termos_relevantes"] = termos_relevantes
    helper["termos_relacionados"] = termos_relacionados
    helper["sinonimos"] = sinonimos
    helper["substantivos_proprios_frase"] = substantivos_proprios_frase

    helper["metricas"] = {}
    helper["metricas"]["m1"] = peso_m1
    helper["metricas"]["m2"] = peso_m2
    helper["metricas"]["m3"] = peso_m3

    # save_as_json(helper, "helper.json")
    return helper


def load_helper(file):
    with open(file, encoding="UTF-8", mode="r") as f:
        values = json.load(f)

    init_helper(values)


def _get_var_name(resource, is_tr=False):
    _resource = resource.lower()
    if _resource in map_resource_to_var:
        return map_resource_to_var[_resource]

    global var_id
    var_name = var_prefixes[is_tr] + str(var_id)
    var_id += 1

    map_resource_to_var[_resource] = var_name
    map_var_to_resource[var_name] = _resource

    return var_name


def _get_var_value(var_name):
    return map_var_to_resource.get(var_name, None)


def _termo_relevante_from_resource(resource):
    _resource = resource.lower()

    tr = map_resource_to_tr.get(_resource, None)

    if tr:
        return _get_var_name(_resource)

    for tr_peso in termos_relevantes:
        tr = tr_peso[0]
        if tr in _resource:
            var_name = _get_var_name(_resource, True)
            map_resource_to_tr[_resource] = tr_peso
            return var_name

    return None


def _termo_relevante_from_var(var_name):
    return map_resource_to_tr.get(_get_var_value(var_name), None)
