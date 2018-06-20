# -*- coding: utf-8 -*-
"""
@project ensepro
@since 10/06/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import os
import subprocess

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def gerar_queries_value_java3(params, step, steps, log=False):
    if (len(params) == 1):
        file_name = params[0]
    else:
        file_name = "resultado_normalizado.json"

    comando = "java -jar " + parent_dir + "/querygenerator.jar " + file_name + " do3"
    if log:
        print("gerando combinações e calculando valores via Java[", comando, "]...", end="", flush=True)

    subprocess.check_output(comando, shell=True)
    if steps.get(step, None):
        if log:
            print("done.")
        return steps[step][0](["queries_renqueadas.json"], steps[step][1], steps, log=log)
