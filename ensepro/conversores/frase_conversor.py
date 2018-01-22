"""
@project ensepro
@since 21/01/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from ensepro.conversores import palavra_conversor
from ensepro.classes.frase import Frase


def from_json(id, json):
    palavras = palavra_conversor.list_palavra_from_json(json)
    return Frase(id=id, palavras=palavras)
