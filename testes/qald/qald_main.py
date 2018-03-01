#!/usr/bin/env python3
"""
@project ensepro
@since 28/02/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import sys
import os


def ensepro_path():
    # Obtém o PATH para a pasta que contém este arquivo
    this_file_directory = os.path.dirname(os.path.abspath(__file__))

    # Volta duas pastas
    ensepro_path = os.path.dirname(this_file_directory)
    ensepro_path = os.path.dirname(ensepro_path)
    # print(ensepro_path)
    return ensepro_path


path = ensepro_path()
sys.path.append(path)

from testes.qald.params import get_args
from testes.qald.qald import execute

args = get_args()
arquivo_qald = args.arquivo_processar
arquivo_resultados = args.arquivo_resultado
mostrar_sinonimos = args.mostrar_sinonimos

execute(arquivo_qald, arquivo_resultados, mostrar_sinonimos)
