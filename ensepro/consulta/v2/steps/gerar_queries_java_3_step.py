# -*- coding: utf-8 -*-
"""
@project ensepro
@since 10/06/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import subprocess


def gerar_queries_value_java3(params, step, steps):
    if (len(params) == 1):
        file_name = params[0]
    else:
        file_name = "resultado_normalizado.json"

    comando = "java -jar querygenerator3.jar " + file_name
    print("gerando combinações e calculando valores via Java[", comando, "]...", end="")

    subprocess.check_output(comando, shell=True)
    if steps.get(step, None):
        print("done.")
        steps[step][0](["gerar_queries_step.json"], steps[step][1], steps)
