# -*- coding: utf-8 -*-
"""
@project ensepro
@since 20/05/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import editdistance
from ensepro.consulta.fields import Field
from ensepro.elasticsearch.searches import list_parcial_match_search
from ensepro.utils.string_utils import remover_acentos
from ensepro.utils.thread_pool import ThreadPool

fields_partial_match = [
    Field.PARTIAL_MATCH_SUJEITO,
    Field.PARTIAL_MATCH_PREDICADO,
    Field.PARTIAL_MATCH_OBJETO
]

TR = ["editora", "einstein"]
if len(sys.argv) > 1:
    TR = [remover_acentos(tr.lower()) for tr in sys.argv[1:]]

var_id = 0
map_vars = {}
map_vars_names = {True: "z", False: "x"}
map_vars_inv = None
distance_edits = {}
map_tr_r = {}

def get_termo_relevante_from(resource):
    vars_values = map_vars.values()
    _resource = resource.lower()

    result = map_tr_r.get(_resource, None)
    if result:
        return result
    if _resource in vars_values:
        return result

    for tr in TR:
        if tr in _resource:
            map_tr_r[_resource] = tr
            result = tr
            break

    return result


def get_termo_relevante(resource):
    _resource = resource.lower()
    return map_tr_r.get(_resource, None)


def calcula_edit_distance(tr, conceito):
    _conceito = conceito.lower()
    existe = distance_edits.get(tr + "-" + _conceito, None)
    if existe:
        return existe

    dist = editdistance.eval(tr, _conceito)
    distance_edits[tr + "-" + _conceito] = dist
    return dist


def get_edit_distance(tr, conceito):
    _conceito = conceito.lower()
    return distance_edits.get(tr + "-" + _conceito, 0)


def get_var_value(var):
    global map_vars_inv
    if map_vars_inv:
        return map_vars_inv[var]

    map_vars_inv = {v: k for k, v in map_vars.items()}
    return map_vars_inv[var]


def get_var_name(value, is_tr=False):
    if value in map_vars:
        return map_vars[value]

    global var_id
    var_name = map_vars_names[is_tr] + str(var_id)
    map_vars[value] = var_name
    var_id += 1
    return var_name


# 1. Search in elasticsearch todos as triplas que contém algum TR
def busca_no_elasticsearch_partial():
    result = list_parcial_match_search(fields_partial_match, TR)
    if result["keys"]:
        return result


# 2. Passar resultado do ES para uma estrutura "utilizável"
def normalize_result(es_result):
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
                # threadpool.add_task(remove_not_tr, tripla)
                result_normalized.append(tripla)

    threadpool.wait_complete()

    return result_normalized


# 3. Remover todas os valores que não são TR, passando estes para um dicionário -> { variável : TR }
def remove_not_tr(tripla):
    ts = True
    tp = True
    to = True

    for tr in TR:
        if ts and tr in tripla[0].lower():
            ts = False
            calcula_edit_distance(tr, tripla[0])
            get_termo_relevante_from(tripla[0])
        if tp and tr in tripla[1].lower():
            tp = False
            calcula_edit_distance(tr, tripla[1])
            get_termo_relevante_from(tripla[1])
        if to and tr in tripla[2].lower():
            to = False
            calcula_edit_distance(tr, tripla[2])
            get_termo_relevante_from(tripla[2])

    tripla[0] = get_var_name(tripla[0], not ts)
    tripla[1] = get_var_name(tripla[1], not tp)
    tripla[2] = get_var_name(tripla[2], not to)


# 4. Realizar "combinações"

def combinacoes(T):
    combinacoes = []
    # print("iniciando combinacoes")
    for t in T:
        combinacoes.append(calculate([t]))
        for t1 in T:
            # threadpool.add_task(add_combinacao, combinacoes, t, t1)
            add_combinacao(combinacoes, t, t1)
    # threadpool.wait_complete()
    return combinacoes


def add_combinacao(combinacoes, t, t1):
    sujeito_igual = t[0] == t1[0]
    predicado_igual = t[1] == t1[1]
    objeto_igual = t[2] == t1[2]
    sujeito_igual_objeto = t[0] == t1[2]
    # 4.1. (s p o)(s p2 o2)
    if sujeito_igual and not predicado_igual and not objeto_igual:
        combinacoes.append(calculate([t, t1]))
    # 4.2. (s p o)(s2 p2 s)
    if not sujeito_igual and not predicado_igual and not objeto_igual and sujeito_igual_objeto:
        combinacoes.append(calculate([t, t1]))


# 5. Fazer cálculos
def calculate(combinacao):
    var_count = 0
    tr_elements = set()
    dist = 0
    for tripla in combinacao:
        for r in tripla:
            resource = get_var_value(r)
            tr = get_termo_relevante(resource)
            if tr:
                dist += get_edit_distance(tr, resource)
                tr_elements.add(tr)
            else:
                var_count += 1

    combinacao.append(var_count)
    combinacao.append(len(tr_elements))
    combinacao.append(dist)

    return combinacao


# 6. Ordenar
def sort(T):
    return sorted(T, key=lambda x: (-x[-2], x[-1], x[-3]))


# Penso que ranqueamento será
# 1. a soma das distâncias de edição para o TR (ou sinônimo) - ascendente
# 2. número de variáveis - ascendente


from ensepro import save_as_json
import time

global_start = time.time()

start = time.time()
print("consultado triplas...")
M = busca_no_elasticsearch_partial()
end = time.time()
print("done -> [", len(M), "]", end - start, "s")

save_as_json(M, "temp_M.json")

start = time.time()
print("normalizando resultados...")
T = normalize_result(M)
end = time.time()
size = len(T)
print("done -> [", size, "]", end - start, "s")

save_as_json(T, "temp_T.json")

start = time.time()
print("gerando combinações e calculando valores... [", size * size, "]... ")
T = combinacoes(T)
end = time.time()
size = len(T)
print("done -> [", size, "]", end - start, "s")

start = time.time()
print("ordenando(ranquenado) triplas...")
T = sort(T)
end = time.time()
print(end - start, "s")

save_as_json(T, "temp_T2.json")
save_as_json(map_vars, "temp_map_vars.json")
save_as_json(distance_edits, "temp_distance_edits.json")
save_as_json(map_tr_r, "temp_map_tr_r.json")

print_results = 20
print("Ordenação feita por: ")
print("1. número de variáveis -> crescente")
print("2. número de TR        -> decrescente")
print("3. soma das distâncias -> crescente")

print("\n\n", (str(print_results) + "/" + str(len(T))), "melhores resultados para:", TR, end="\n\n")
for t in T[:print_results]:
    print(t)

print("Time to process:", end - global_start, "s")
