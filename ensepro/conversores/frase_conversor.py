# -*- coding: utf-8 -*-
"""
@project ensepro
@since 25/02/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from ensepro.conversores import palavra_conversor
from ensepro.classes.frase import Frase


def from_json(id, frase_texto, json):
    palavras = palavra_conversor.list_palavra_from_json(json)
    return Frase(id=id, frase=frase_texto, palavras=palavras)
