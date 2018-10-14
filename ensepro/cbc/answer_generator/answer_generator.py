# -*- coding: utf-8 -*-
"""
@project ensepro
@since 08/06/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
from ensepro import LoggerConstantes
from ensepro.cbc.answer_generator.steps.elastic_search_step import elastic_search_step, elastic_search_integrado_step
from ensepro.cbc.answer_generator.steps.normalizar_step import normalizar_step, normalizar_value_step
from ensepro.cbc.answer_generator.steps.print_resultado_step import print_resultado
from ensepro.cbc.answer_generator.steps.answer_generator_step import answer_generator_step

logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_ANSWER_GENERATOR)

actions = {
    "-elasticsearch-integrado": elastic_search_integrado_step,
    "-elasticsearch-java": elastic_search_step,
    "-normalizar-java": normalizar_step,
    "-gerar-java": answer_generator_step,
}

actions_next = {
    "-elasticsearch-integrado": (normalizar_value_step, "-normalizar-java"),
    "-elasticsearch-java": (normalizar_value_step, "-normalizar-java"),
    "-normalizar-java": (answer_generator_step, "-gerar-java"),
    "-gerar-java": (print_resultado, None),
}

start_at = "-elasticsearch-java"


def get(frase):
    action_to_execute = actions.get(start_at)
    termos_relevantes = obtem_termos_relevantes_frase(frase)
    return action_to_execute(termos_relevantes, start_at, actions_next)


def execute_integration(params):
    step = "-elasticsearch-integrado"
    action_to_execute = actions.get(step)
    logger.debug("Answer Generator - Executando step %s", step)
    return action_to_execute(params, step, actions_next)


def obtem_termos_relevantes_frase(frase):
    return [palavra.palavra_canonica for palavra in frase.termos_relevantes]
