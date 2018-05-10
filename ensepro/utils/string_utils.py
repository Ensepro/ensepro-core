# -*- coding: utf-8 -*-
"""
@project ensepro
@since 25/02/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
isascii = lambda word: len(word) == len(word.encode())


def remover_acentos(text: str):
    from unicodedata import normalize
    return normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')


def tem_acentuacao(text: str):
    return not isascii(text)
