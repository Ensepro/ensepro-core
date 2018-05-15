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

fields_partial_match = [
    Field.PARTIAL_MATCH_SUJEITO,
    Field.PARTIAL_MATCH_PREDICADO,
    Field.PARTIAL_MATCH_OBJETO
]

TR = ["default1", "default2"]
if len(sys.argv) > 1:
    TR = sys.argv[1:]

var_id = 0
map_vars = {}
distance_edits = {}


def calcula_edit_distance(tr, conceito):
    existe = distance_edits.get(tr + "-" + conceito, None)
    if existe:
        return existe

    dist = editdistance.eval(tr, conceito)
    distance_edits[tr + "-" + conceito] = dist
    return dist


def get_var_name(value):
    if value in map_vars:
        return map_vars[value]

    global var_id
    var_name = "x" + str(var_id)
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
            sujeito = result_tripla["_source"]["sujeito"]["conceito"]
            predicado = result_tripla["_source"]["predicado"]["conceito"]
            objeto = result_tripla["_source"]["objeto"]["conceito"]

            tripla = [sujeito, predicado, objeto]

            tripla_ja_existe = triplas.get(tripla[0] + "-" + tripla[1] + "-" + tripla[2], None)
            if tripla_ja_existe:
                continue

            triplas[tripla[0] + "-" + tripla[1] + "-" + tripla[2]] = tripla
            remove_not_tr(tripla)
            result_normalized.append(tripla)

    return result_normalized


# 3. Remover todas os valores que não são TR, passando estes para um dicionário -> { variável : TR }
def remove_not_tr(tripla):
    ts = True
    tp = True
    to = True

    for tr in TR:
        if ts and tr in tripla[0].lower():
            ts = False
            calcula_edit_distance(tr, tripla[0].lower())
        if tp and tr in tripla[1].lower():
            tp = False
            calcula_edit_distance(tr, tripla[1].lower())
        if to and tr in tripla[2].lower():
            to = False
            calcula_edit_distance(tr, tripla[2].lower())

    if ts:
        tripla[0] = get_var_name(tripla[0])

    if tp:
        tripla[1] = get_var_name(tripla[1])

    if to:
        tripla[2] = get_var_name(tripla[2])


# 4. Realizar "combinações"

def combinacoes(T):
    combinacoes = []
    for t in T:
        combinacoes.append([t])
        for t1 in T:
            sujeito_igual = t[0] == t1[0]
            predicado_igual = t[1] == t1[1]
            objeto_igual = t[2] == t1[2]
            sujeito_igual_objeto = t[0] == t1[2]

            # 4.1. (s p o)(s p2 o2)
            if sujeito_igual and not predicado_igual and not objeto_igual:
                combinacoes.append([t, t1])

            # 4.2. (s p o)(s2 p2 s)
            if not sujeito_igual and not predicado_igual and not objeto_igual and sujeito_igual_objeto:
                combinacoes.append([t, t1])

    return combinacoes


# 5. Fazer cálculos
def calculate(combinacoes):
    values = map_vars.values()
    for combinacao in combinacoes:
        var_count = 0
        tr_elements = set()
        dist = 0
        for tripla in combinacao:
            for r in tripla:
                if r in values:
                    var_count += 1
                else:
                    for tr in TR:
                        if tr in r.lower():
                            tr_elements.add(tr)
                            dist += calcula_edit_distance(tr, r.lower())
                            break

        combinacao.append(var_count)
        combinacao.append(len(tr_elements))
        combinacao.append(dist)


# 6. Ordenar
def sort(T):
    return sorted(T, key=lambda x: (-x[-2], x[-1], x[-3]))


# Penso que ranqueamento será
# 1. a soma das distâncias de edição para o TR (ou sinônimo) - ascendente
# 2. número de variáveis - ascendente


from ensepro import save_as_json

print("consultado triplas...")
M = busca_no_elasticsearch_partial()
save_as_json(M, "temp_M.json")

print("normalizando resultados...")
T = normalize_result(M)
save_as_json(T, "temp_T.json")

print("gerando combinações...")
T = combinacoes(T)

print("calculando valores...")
calculate(T)

print("ordenando(ranquenado) triplas...")
T = sort(T)

save_as_json(T, "temp_T2.json")
save_as_json(map_vars, "temp_map_vars.json")
save_as_json(distance_edits, "temp_distance_edits.json")

print_results = 20
print("Ordenação feita por: ")
print("1. número de TR        -> decrescente")
print("2. soma das distâncias -> crescente")
print("3. número de variáveis -> crescente")
print("\n\n", (str(print_results) + "/" + str(len(T))), "melhores resultados para:", TR, end="\n\n")
for t in T[:print_results]:
    print(t)
