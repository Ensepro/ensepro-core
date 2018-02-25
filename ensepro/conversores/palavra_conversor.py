# -*- coding: utf-8 -*-
"""
@project ensepro
@since 25/02/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
from ensepro.classes.palavra import Palavra


def list_palavra_from_json(json) -> list:
    palavras = []
    for json_palavra in json:
        id = len(palavras) + 1
        palavra = palavra_from_json(id, json_palavra)
        palavras.append(palavra)

    return palavras


def palavra_from_json(id, json):
    return Palavra(id=id, dados_palavra=json)
