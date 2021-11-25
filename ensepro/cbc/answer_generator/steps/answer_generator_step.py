# -*- coding: utf-8 -*-
"""
@project ensepro
@since 10/06/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import subprocess, sys, time
import ensepro.configuracoes as configuracoes
from ensepro import ConsultaConstantes, LoggerConstantes

lca_size = configuracoes.get_config(ConsultaConstantes.LCA_SIZE)
slm1_factor = configuracoes.get_config(ConsultaConstantes.SLM1_FACTOR)
slm1_factor_only_l1 = configuracoes.get_config(ConsultaConstantes.SLM1_FACTOR_ONLY_L1)
threads = configuracoes.get_config(ConsultaConstantes.THREADS_ANSWER_GENERATOR)
path_answer_generator = configuracoes.get_config(ConsultaConstantes.PATH_ANSWER_GENERATOR)

logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_ANSWER_GENERATOR_STEP)


def answer_generator_step(params, step, steps):
    file_name = params[0] if len(params) == 1 else "resultado_normalizado.json"

    comando = ' '.join([
        "java -jar",
        path_answer_generator,
        file_name,
        str(lca_size if lca_size > 0 else sys.maxsize),
        str(threads),
        str(params["nivel_combination"]),
        str(slm1_factor),
        "true" if slm1_factor_only_l1 else "false"
    ])

    logger.debug("Gerando combinações e calculando valores via Java[%s]", comando)

    start = time.time_ns()
    subprocess.check_output(comando, shell=True)
    end = time.time_ns()

    if steps.get(step, None):
        logger.debug("Chamando próximo passo: %s", steps[step][1])
        return steps[step][0](["queries_renqueadas.json", params["frase"], params["frase_analisada"], (end - start), params["helper"]], steps[step][1], steps)
