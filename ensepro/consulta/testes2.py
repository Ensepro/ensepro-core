# -*- coding: utf-8 -*-
"""
@project ensepro
@since 24/05/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import concurrent
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import editdistance
from ensepro.consulta.fields import Field
from ensepro.elasticsearch.searches import list_parcial_match_search
from ensepro.utils.string_utils import remover_acentos

fields_partial_match = [
    Field.PARTIAL_MATCH_SUJEITO,
    Field.PARTIAL_MATCH_PREDICADO,
    Field.PARTIAL_MATCH_OBJETO
]

TERMOS_RELEVANTES_PESOS = ["editorapt", 1, "einstein", 1]
if len(sys.argv) > 1:
    TERMOS_RELEVANTES_PESOS = [remover_acentos(tr.lower()) for tr in sys.argv[1:]]

TERMOS_RELEVANTES = []
PESOS = {}

for index, termo in enumerate(TERMOS_RELEVANTES_PESOS):
    if (index + 1) % 2 == 0:
        PESOS[TERMOS_RELEVANTES_PESOS[index - 1]] = termo
    else:
        TERMOS_RELEVANTES.append(termo)

map_resource_to_var = {}
map_var_to_resource = {}
map_distancias_edicao = {}
map_resource_to_tr = {}

var_id = 1
var_prefixes = {True: "z", False: "x"}


def _get_var_name(_resource, is_tr=False):
    # _resource = resource.lower()
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


def _termo_relevante_from_resource(_resource):
    # _resource = resource.lower()

    tr = map_resource_to_tr.get(_resource, None)

    if tr:
        return _get_var_name(_resource)

    _resource_lower = _resource.lower()
    for tr in TERMOS_RELEVANTES:
        if tr in _resource_lower:
            var_name = _get_var_name(_resource, True)
            map_resource_to_tr[_resource] = tr
            _calcular_distancia_edicao(tr, var_name)
            return var_name

    return None


def _termo_relevante_from_var(var_name):
    return map_resource_to_tr.get(_get_var_value(var_name), None)


# 1. Search in elasticsearch todos as triplas que contém algum TR
def busca_no_elasticsearch_partial(termos_Relevantes):
    print("consultando triplas... ", end="")
    result = list_parcial_match_search(fields_partial_match, termos_Relevantes)
    if result["keys"]:
        print("done.", end="")
        return result

    raise Exception("Nenhuma tripla encontrada para termos relevantes: ", TERMOS_RELEVANTES)


# 2. Passar resultado do ES para uma estrutura "utilizável"
def normalize_result(es_result):
    print("normalizando resultados... ", end="")
    triplas = {}
    result_normalized = []
    result = es_result["result"]
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

    print("done -> size=", len(result_normalized), end="")
    return result_normalized


# 3. Remover todas os valores que não são TR, passando estes para um dicionário -> { variável : TR }
def alterar_para_variaveis(tripla):
    for index in range(len(tripla)):
        tr = _termo_relevante_from_resource(tripla[index])
        if tr:
            tripla[index] = tr
        else:
            tripla[index] = _get_var_name(tripla[index])


# 4. Realizar "combinações"
def combinacoes(T):
    print("gerando combinações e calculando valores... ", end="", flush=True)
    combinacoes = []
    for t in T:
        combinacoes.append(calcular_metricas([t]))
        do_combinacoes(combinacoes, T, t)

    print("done -> size=", len(combinacoes), end="")
    return combinacoes


def do_combinacoes(combinacoes, T, t):
    for t1 in T:
        add_combinacao(combinacoes, t, t1)


def add_combinacao(combinacoes, tripla1, tripla2):
    # sujeito_igual
    if tripla1[0] == tripla2[0]:
        # predicado_igual
        if tripla1[1] == tripla2[1]:
            return
        # objeto_igual
        if tripla1[2] == tripla2[2]:
            return

        # 4.1. (s p o)(s p2 o2)
    else:
        # predicado_igual
        if tripla1[1] == tripla2[1]:
            return
        # objeto_igual
        if tripla1[2] == tripla2[2]:
            return
        # sujeito_igual_objeto
        if tripla1[0] != tripla2[2]:
            return
        # 4.2. (s p o)(s2 p2 s)

    combinacoes.append(calcular_metricas([tripla1, tripla2]))


# 5. Fazer cálculos
def calcular_metricas(combinacao):
    var_count = 0
    tr_elements = set()
    some_distancias = 0
    for tripla in combinacao:
        for resource_var_name in tripla:
            tr = _termo_relevante_from_var(resource_var_name)
            if tr:
                some_distancias += _calcular_distancia_edicao(tr, resource_var_name)
                tr_elements.add(tr)
            else:
                var_count += 1

    calc_tr = 0
    for t in tr_elements:
        calc_tr += PESOS[t]

    combinacao.append(var_count)
    combinacao.append(calc_tr)
    combinacao.append(some_distancias)

    return combinacao


# 6. Ordenar
def sort(T):
    print("ordenando(ranquenado) triplas... ", end="")
    t_sorted = sorted(T, key=lambda x: (-x[-2], x[-1], x[-3]))
    print("done.", end="")
    return t_sorted


def print_resultados(resultado_anterior):
    print("\n\nExibindo os 20 melhores resultados para:", TERMOS_RELEVANTES)
    resultados_para_printar = resultado_anterior[:20]

    print()
    for resultado in resultados_para_printar:
        for tripla in resultado:
            if type(tripla) is list:
                for index in range(len(tripla)):
                    if tripla[index][0] == "z":
                        tripla[index] = _get_var_value(tripla[index])

        print(resultado)


steps = [
    busca_no_elasticsearch_partial,
    normalize_result,
    combinacoes,
    sort,
    print_resultados
]
resultado_anterior = TERMOS_RELEVANTES
import time

for step in steps:
    start = time.time()
    resultado_anterior = step(resultado_anterior)
    print(" -> ", time.time() - start)
