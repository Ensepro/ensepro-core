# -*- coding: utf-8 -*-
"""
@project ensepro
@since 09/05/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""


def get_ensepro_path(file):
    import os
    # Obtém o PATH para a pasta que contém este arquivo
    this_file_directory = os.path.dirname(os.path.abspath(file))

    # Volta um diretório
    ensepro_path = os.path.dirname(this_file_directory)
    return ensepro_path
