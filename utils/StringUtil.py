"""
@project ensepro
@since 19/07/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import unicodedata


def isEmpty(string):
    temp = (string is None or string == '' or string.replace(" ", "") == '')
    return temp

#TODO: refazer este método
def removeStrings(strings, fromString, toString):
    for string in strings:
        fromString = fromString.replace(string, toString)
    return fromString

#TODO: renomar para um nome melhor
def getElementosIguaisDeDuasListas(lista1, lista2):
    return list(set(lista1).intersection(lista2))

#TODO: revisar
def removeAcentuacao(texto):
    return ''.join((c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn'))

#TODO: comentar e renomear variáveis
def find(a, b):
    for i in range(len(a)):
        if(b == a[i]):
            return i
    return -1