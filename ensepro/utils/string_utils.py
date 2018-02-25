# -*- coding: utf-8 -*-
"""
@project ensepro
@since 25/02/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""


def remover_acentos(txt):
    from unicodedata import normalize
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')
