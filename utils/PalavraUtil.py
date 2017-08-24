"""
@project ensepro
@since 23/08/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""


def isMesmaClasseGramatical(palavra, sinonimo) -> bool:
    if palavra.isVerbo():
        return sinonimo.classeGramatical == "v"

    if palavra.isAdjetivo():
        return sinonimo.classeGramatical == "a"

    if palavra.isSubstantivo():
        return sinonimo.classeGramatical == "n"

    return False
