# -*- coding: utf-8 -*-
"""
@project ensepro
@since 08/06/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

if __name__ == '__main__':
    import os
    import sys

    THIS_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    sys.path.append(THIS_PATH)

from ensepro.cbc.answer_generator.steps.elastic_search_step import elastic_search_step, elastic_search_integrado_step
from ensepro.cbc.answer_generator.steps.normalizar_step import normalizar_step, normalizar_value_step
from ensepro.cbc.answer_generator.steps.print_resultado_step import print_resultado, print_resultado_value
from ensepro.cbc.answer_generator.steps.gerar_queries_java_2_step import gerar_queries_value_java2
from ensepro.cbc.answer_generator.steps.gerar_queries_java_3_step import gerar_queries_value_java3

actions = {
    "-elasticsearch-integrado": elastic_search_integrado_step,
    "-elasticsearch-java2": elastic_search_step,
    "-elasticsearch-java3": elastic_search_step,
    "-normalizar-java2": normalizar_step,
    "-normalizar-java3": normalizar_step,
    "-gerar-java2": gerar_queries_value_java2,
    "-gerar-java3": gerar_queries_value_java3
}

actions_next = {
    "-elasticsearch-integrado": (normalizar_value_step, "-normalizar-java2"),
    "-elasticsearch-java2": (normalizar_value_step, "-normalizar-java2"),
    "-elasticsearch-java3": (normalizar_value_step, "-normalizar-java3"),

    "-normalizar-java2": (gerar_queries_value_java2, "-gerar-java2"),
    "-normalizar-java3": (gerar_queries_value_java3, "-gerar-java3"),

    "-gerar-java2": (print_resultado, None),
    "-gerar-java3": (print_resultado, None)
}

if __name__ == '__main__':

    if len(sys.argv) <= 1:
        print("Passagem de parametros obrigatória. -help para ajuda")
        exit(10)

    action_selected = sys.argv[1]
    action_to_execute = actions.get(action_selected, None)

    if action_to_execute:
        action_to_execute(sys.argv[2:], action_selected, actions_next, log=True)
    else:
        print("Ação não mapeada.")

start_at = "-elasticsearch-java2"


def get(frase):
    action_to_execute = actions.get(start_at)
    termos_relevantes = obtem_termos_relevantes_frase(frase)
    return action_to_execute(termos_relevantes, start_at, actions_next)


def execute_integration(params):
    step = "-elasticsearch-integrado"
    action_to_execute = actions.get(step)
    return action_to_execute(params, step, actions_next)


def obtem_termos_relevantes_frase(frase):
    return [palavra.palavra_canonica for palavra in frase.termos_relevantes]
