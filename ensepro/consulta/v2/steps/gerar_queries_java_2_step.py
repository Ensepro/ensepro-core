# -*- coding: utf-8 -*-
"""
@project ensepro
@since 10/06/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import subprocess
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def gerar_queries_value_java2(params, step, steps, log=False):
    if (len(params) == 1):
        file_name = params[0]
    else:
        file_name = "resultado_normalizado.json"

    comando = "java -jar " + parent_dir + "/querygenerator2.jar " + file_name
    if log:
        print("gerando combinações e calculando valores via Java[", comando, "]...", end="")

    subprocess.check_output(comando, shell=True)
    if steps.get(step, None):
        if log:
            print("done.")
        return steps[step][0](["gerar_queries_step.json"], steps[step][1], steps, log=log)
