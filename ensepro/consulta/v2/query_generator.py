# -*- coding: utf-8 -*-
"""
@project ensepro
@since 08/06/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import os
import sys

THIS_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(THIS_PATH)

from ensepro.consulta.v2.steps.elastic_search_step import elastic_search_step
from ensepro.consulta.v2.steps.normalizar_step import normalizar_step, normalizar_value_step
from ensepro.consulta.v2.steps.gerar_queries_step import gerar_queries, gerar_queries_value
from ensepro.consulta.v2.steps.print_resultado_step import print_resultado, print_resultado_value
from ensepro.consulta.v2.steps.ranquear_step import ranquear_step, ranquear_step_value
from ensepro.consulta.v2.steps.show_help import show_help

actions = {
    "-help": show_help,
    "-elasticsearch": elastic_search_step,
    "-normalizar": normalizar_step,
    "-gerar": gerar_queries,
    "-ranquear": ranquear_step,
    "-printar-resultados": print_resultado
}

actions_next = {
    "-help": (None, None),
    "-elasticsearch": (normalizar_value_step, "-normalizar"),
    "-normalizar": (gerar_queries_value, "-gerar"),
    "-gerar": (ranquear_step_value, "-ranquear"),
    "-ranquear": (print_resultado_value, None)
}

if len(sys.argv) <= 1:
    print("Passagem de parametros obrigatória. -help para ajuda")
    exit(10)

action_selected = sys.argv[1]
action_to_execute = actions.get(action_selected, None)

if action_to_execute:
    action_to_execute(sys.argv[2:], action_selected, actions_next)
else:
    print("Ação não mapeada.")
