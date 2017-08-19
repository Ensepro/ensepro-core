"""
@project ensepro
@since 19/07/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from constantes.StringConstantes import UTF_8


def toUTF8(string):
    return string.decode(UTF_8)
