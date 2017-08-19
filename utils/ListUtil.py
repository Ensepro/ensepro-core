"""
@project ensepro
@since 05/08/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""


def mergeListas(lista1, lista2):
    return lista1 + list(set(lista2) - set(lista1))


# TODO: renomar para um nome melhor
def getElementosIguaisDeDuasListas(lista1, lista2):
    return list(set(lista1).intersection(lista2))
