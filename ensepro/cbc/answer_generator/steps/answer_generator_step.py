# -*- coding: utf-8 -*-
"""
@project ensepro
@since 10/06/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import subprocess
import ensepro.configuracoes as configuracoes
from ensepro import ConsultaConstantes, LoggerConstantes

numero_respostas = configuracoes.get_config(ConsultaConstantes.NUMERO_RESPOSTAS)
threads = configuracoes.get_config(ConsultaConstantes.THREADS_ANSWER_GENERATOR)
path_answer_generator = configuracoes.get_config(ConsultaConstantes.PATH_ANSWER_GENERATOR)

logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_ANSWER_GENERATOR_STEP)


def answer_generator_step(params, step, steps):
    file_name = params[0] if len(params) == 1 else "resultado_normalizado.json"

    comando = ' '.join([
        "java -jar",
        path_answer_generator,
        file_name,
        str(numero_respostas),
        str(threads),
        str(params["nivel_combination"])
    ])

    logger.debug("Gerando combinações e calculando valores via Java[%s]", comando)

    subprocess.check_output(comando, shell=True)
    if steps.get(step, None):
        logger.debug("Chamando próximo passo: %s", steps[step][1])
        return steps[step][0](["queries_renqueadas.json", params["frase"]], steps[step][1], steps)
