# -*- coding: utf-8 -*-
"""
@project ensepro
@since 08/06/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from ensepro import save_as_json
import json
from ensepro.cbc.query_generator import helper


def gerar_queries_value(params, step, steps, log=False):
    if log:
        print("gerando combinações e calculando valores... ", end="")

    helper.init_helper(params["helper"])

    triplas = params["values"]

    queries = []
    for t in triplas:
        queries.append([t])
        do_combinacoes_2(queries, triplas, t)

    if log:
        print("done -> size=", len(queries))

    if steps.get(step, None):
        values = {}
        values["helper"] = helper.save_helper()
        values["values"] = queries
        save_as_json(values, "gerar_queries_step.json")
        return steps[step][0](values, steps[step][1], steps, log=log)
    else:
        return queries


def gerar_queries(params, step, steps, log=False):
    with open(params[0], encoding="UTF-8", mode="r") as f:
        value = json.load(f)

    return gerar_queries_value(value, step, steps, log=log)


def do_combinacoes_2(combinacoes, T, t):
    for t1 in T:
        add_combinacao_2(combinacoes, t, t1)
        # do_combinacoes_3(combinacoes, T, t, t1)


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
        combinacoes.append([tripla1, tripla2, tripla3])
        return

    if sujeito1_igual_sujeito2 and objeto2_igual_sujeito3 and predicados_todos_diferentes and objetos_todos_diferentes and not \
            sujeito2_igual_sujeito3:
        # 4.6.
        combinacoes.append([tripla1, tripla2, tripla3])
        return

    if objeto1_igual_sujeito2 and sujeito2_igual_sujeito3 and predicado2_igual_predicado3 and objetos_todos_diferentes and not \
            predicado1_igual_predicado2 and not sujeitos_iguais:
        # 4.7.
        combinacoes.append([tripla1, tripla2, tripla3])
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
        combinacoes.append([tripla1, tripla2])
        return

    if sujeito_diferente and predicado_diferente and objeto_diferente and sujeito_igual_objeto:
        combinacoes.append([tripla1, tripla2])
        return

    if sujeito_diferente and predicado_igual and objeto_igual:
        combinacoes.append([tripla1, tripla2])
        return
