"""
@project ensepro
@since 19/07/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import unicodedata


isascii = lambda word: len(word) == len(word.encode())



def regexExistIn(regex, string):
    return regex.search(string) is not None


def isEmpty(string):
    return (string is None or string == '' or string.replace(" ", "") == '')


# TODO: revisar
def removeAccentuation(texto):
    return ''.join((c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn'))

def hasAccentuation(word):
    return not isascii(word)


# TODO: comentar e renomear variáveis
def find(a, b):
    for i in range(len(a)):
        if (b == a[i]):
            return i
    return -1
