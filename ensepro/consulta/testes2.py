# -*- coding: utf-8 -*-
"""
@project ensepro
@since 24/05/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
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

TERMOS_RELEVANTES_PESOS = ["volume", '1', "america_latina", '1']
if len(sys.argv) > 1:
    TERMOS_RELEVANTES_PESOS = [remover_acentos(tr.lower()) for tr in sys.argv[1:]]

TERMOS_RELEVANTES = []
PESOS = {}

for index, termo in enumerate(TERMOS_RELEVANTES_PESOS):
    if (index + 1) % 2 == 0:
        PESOS[TERMOS_RELEVANTES_PESOS[index - 1]] = int(termo)
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
        do_combinacoes_2(combinacoes, T, t)

    print("done -> size=", len(combinacoes), end="")
    return combinacoes


def do_combinacoes_2(combinacoes, T, t):
    for t1 in T:
        add_combinacao_2(combinacoes, t, t1)
        #do_combinacoes_3(combinacoes, T, t, t1)


def do_combinacoes_3(combinacoes, T, t, t1):
    for t2 in T:
        add_combinacao_3(combinacoes, t, t1, t2)


def add_combinacao_3(combinacoes, tripla1, tripla2, tripla3):
    # 4.5. (Z1      )(Z1    Z2)(      Z2)
    # 4.6. (Z1      )(Z1    Z2)(Z2      )
    # 4.7. (      Z1)(Z1 Z2   )(Z1 Z2   )

    sujeito1_igual_sujeito2 = tripla1[0] == tripla2[0]
    sujeito2_igual_sujeito3 = tripla2[0] == tripla3[0]
    sujeito1_igual_sujeito3 = tripla1[0] == tripla3[0]

    predicado1_igual_predicado2 = tripla1[1] == tripla2[1]
    predicado2_igual_predicado3 = tripla2[1] == tripla3[1]
    predicado1_igual_predicado3 = tripla1[1] == tripla3[1]

    objeto1_igual_objeto2 = tripla1[2] == tripla2[2]
    objeto2_igual_objeto3 = tripla2[2] == tripla3[2]
    objeto1_igual_objeto3 = tripla1[2] == tripla3[2]

    objeto1_igual_sujeito2 = tripla1[2] == tripla2[0]
    objeto2_igual_sujeito3 = tripla2[2] == tripla3[0]

    sujeitos_iguais = sujeito1_igual_sujeito2 and sujeito2_igual_sujeito3
    predicados_iguais = predicado1_igual_predicado2 and predicado2_igual_predicado3
    objetos_iguais = objeto1_igual_objeto2 and objeto2_igual_objeto3

    sujeitos_todos_diferentes = not sujeito1_igual_sujeito2 and not sujeito2_igual_sujeito3 and not sujeito1_igual_sujeito3
    predicados_todos_diferentes = not predicado1_igual_predicado2 and not predicado2_igual_predicado3 and not predicado1_igual_predicado3
    objetos_todos_diferentes = not objeto1_igual_objeto2 and not objeto2_igual_objeto3 and not objeto1_igual_objeto3

    if sujeitos_iguais and predicados_iguais and objetos_iguais:
        return

    if sujeito1_igual_sujeito2 and objeto2_igual_objeto3 and predicados_todos_diferentes and not objeto1_igual_objeto2:
        # 4.5.
        combinacoes.append(calcular_metricas([tripla1, tripla2, tripla3]))
        return

    if sujeito1_igual_sujeito2 and objeto2_igual_sujeito3 and predicados_todos_diferentes and objetos_todos_diferentes and not \
            sujeito2_igual_sujeito3:
        # 4.6.
        combinacoes.append(calcular_metricas([tripla1, tripla2, tripla3]))
        return

    if objeto1_igual_sujeito2 and sujeito2_igual_sujeito3 and predicado2_igual_predicado3 and objetos_todos_diferentes and not \
            predicado1_igual_predicado2 and not sujeitos_iguais:
        # 4.7.
        combinacoes.append(calcular_metricas([tripla1, tripla2, tripla3]))
        return


def add_combinacao_2(combinacoes, tripla1, tripla2):
    # 4.1.(Z1      ) (Z1      )
    # 4.2.(      Z1) (Z1      )
    # 4.3.(   Z1 Z2) (   Z1 Z2)

    sujeito_igual = tripla1[0] == tripla2[0]
    predicado_igual = tripla1[1] == tripla2[1]
    objeto_igual = tripla1[2] == tripla2[2]

    sujeito_diferente = not sujeito_igual
    predicado_diferente = not predicado_igual
    objeto_diferente = not objeto_igual

    sujeito_igual_objeto = tripla1[0] == tripla2[2]

    if sujeito_igual and predicado_diferente and objeto_diferente:
        combinacoes.append(calcular_metricas([tripla1, tripla2]))
        return

    if sujeito_diferente and predicado_diferente and objeto_diferente and sujeito_igual_objeto:
        combinacoes.append(calcular_metricas([tripla1, tripla2]))
        return

    if sujeito_diferente and predicado_igual and objeto_igual:
        combinacoes.append(calcular_metricas([tripla1, tripla2]))
        return


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
    v = set()
    print()
    for resultado in resultados_para_printar:
        for tripla in resultado:
            if type(tripla) is list:
                for index in range(len(tripla)):
                    if tripla[index][0] == "z":
                        tripla[index] = _get_var_value(tripla[index])
                    elif tripla[index][0] == "x":
                        v.add(tripla[index])

        print(resultado)

    for v1 in v:
        print(v1, "=", _get_var_value(v1))


steps = [
    busca_no_elasticsearch_partial,
    normalize_result,
    combinacoes,
    sort,
    print_resultados
]

resultado_anterior = TERMOS_RELEVANTES
import time
from ensepro import save_as_json
valor = 1
for step in steps:
    start = time.time()
    resultado_anterior = step(resultado_anterior)
    save_as_json(resultado_anterior, "resultado"+str(valor)+".json")
    valor += 1
    print(" -> ", time.time() - start)


save_as_json(map_var_to_resource, "variaveis.json")
