# -*- coding: utf-8 -*-
"""
@project ensepro
@since 08/06/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
from ensepro import save_as_json
import editdistance
import json

map_resource_to_var = {}
map_var_to_resource = {}
map_distancias_edicao = {}
map_resource_to_tr = {}
termos_relevantes = []

var_id = 1
var_prefixes = {True: "z", False: "x"}


def init_helper(values):
    global map_resource_to_var
    global map_var_to_resource
    global map_distancias_edicao
    global map_resource_to_tr
    global termos_relevantes

    map_resource_to_var = values.get("map_resource_to_var", map_resource_to_var)
    map_var_to_resource = values.get("map_var_to_resource", map_var_to_resource)
    map_distancias_edicao = values.get("map_distancias_edicao", map_distancias_edicao)
    map_resource_to_tr = values.get("map_resource_to_tr", map_resource_to_tr)
    termos_relevantes = values.get("termos_relevantes", termos_relevantes)


def save_helper():
    helper = {}
    helper["map_resource_to_var"] = map_resource_to_var
    helper["map_var_to_resource"] = map_var_to_resource
    helper["map_distancias_edicao"] = map_distancias_edicao
    helper["map_resource_to_tr"] = map_resource_to_tr
    helper["termos_relevantes"] = termos_relevantes

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


def _calcular_distancia_edicao(termo_relevante, var_name):
    key = termo_relevante + "-" + var_name
    ja_calculado = map_distancias_edicao.get(key, None)
    if ja_calculado is not None:
        return ja_calculado

    de = editdistance.eval(termo_relevante, _get_var_value(var_name))
    map_distancias_edicao[key] = de
    return de


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
            _calcular_distancia_edicao(tr, var_name)
            return var_name

    return None


def _termo_relevante_from_var(var_name):
    return map_resource_to_tr.get(_get_var_value(var_name), None)
