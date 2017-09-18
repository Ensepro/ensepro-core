"""
@project ensepro
@since 18/09/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>





# TODO: Revisar código
"""

from bean.Frase import Frase
from nltk.tree import *
from constantes.StringConstantes import FILE_WRITE_READ
from constantes.StringConstantes import UTF_8


# <Métodos considerando lista como árore>
def getTree(frase: Frase):
    """
    Méotodo que cria uma ávore(nltk.Tree) com a estrura de árvore retornados do Palavras. Nós contém o seguinte formato: "(<TagInicial>'|'<numero>'| '<PalavraOriginal>)"
    :return: Um objeto da classe nltk.Tree
    """
    formatToParse = "(" + _montaArvore(frase, -1, "", frase.palavras, 0) + ")"
    return Tree.fromstring(formatToParse)


def printTreeFormat(frase: Frase, fileName: str):
    """
    Printa a árvore de forma "bonitinha" utilizando o método pretty_print() da classe nltk.Tree
    :return: None
    """
    tree = getTree(frase)
    file = open(fileName, FILE_WRITE_READ, encoding=UTF_8)
    tree.pretty_print(stream=file)
    file.close()


def isNoTerminal(frase: Frase, numero: int):
    """
    Verifica se uma palavra é um nó terminal.
    :param numero: Número(id) da palavra a ser verificada.
    :return: <True> se for um nó terminal. <False> caso não for um nó terminal.
    """
    indicePalavra = _buscarIndicePorNumero(frase, numero)
    if (indicePalavra == -1):
        print("Palavra com numero=" + str(numero) + " não encontrado!")
        return False
    if (indicePalavra == len(frase.palavras) - 1):
        return True

    thisNivel = int(frase.palavras[indicePalavra].nivel)
    nextNivel = int(frase.palavras[indicePalavra + 1].nivel)

    if (thisNivel == nextNivel):
        return True
    if (thisNivel > nextNivel):
        return True
    return False


def isNoNaoTerminal(self, numero: int):
    """
    Verifica se uma palavra é um nó não terminal.
    :param numero: Número(id) da palavra a ser verificada.
    :return: <True> se for um nó não terminal. <False> caso for um nó não terminal.
    """
    return not self.isNoTerminal(numero)


def _montaArvore(frase: Frase, nivelAnterior, arvore, lista, i):
    """

    :param nivelAnterior: Nível da palavra i-1
    :param arvore: arvore(uma string) onde será concatenado as palavras agrupadas por parenteses
    :param lista: lista de palavras
    :param i: iterator para navegar na lista de palavras
    :return: uma string, com a árvore agrupada por parenteses para conversão em árvore da classe nltk.Tree
    """
    if (i + 1 > len(lista)):
        return arvore + (")" * nivelAnterior)
    thisNivel = int(lista[i].nivel)

    if (thisNivel > nivelAnterior):
        if ((i + 1) < len(lista) and thisNivel == int(lista[i + 1].nivel)):
            arvore = arvore + "(" + lista[i].tagInicial + "|" + str(lista[i].numero) + "| " + lista[i].palavraOriginal + ")"
        else:
            arvore = arvore + "(" + lista[i].tagInicial + "|" + str(lista[i].numero) + "| " + lista[i].palavraOriginal + ""
        return _montaArvore(frase, thisNivel, arvore, lista, i + 1)

    if (thisNivel == nivelAnterior):
        if ((i + 1) < len(lista) and int(lista[i + 1].nivel) > thisNivel):
            arvore = arvore + " (" + lista[i].tagInicial + "|" + str(lista[i].numero) + "| " + lista[i].palavraOriginal + ""
        else:
            arvore = arvore + " (" + lista[i].tagInicial + "|" + str(lista[i].numero) + "| " + lista[i].palavraOriginal + ")"
        return _montaArvore(frase, thisNivel, arvore, lista, i + 1)

    if (thisNivel < nivelAnterior):
        arvore = arvore + (")" * (nivelAnterior - thisNivel))
        return _montaArvore(frase, thisNivel, arvore, lista, i)


# </Métodos considerando lista como árore>


def _buscarIndicePorNumero(frase: Frase, numero: int):
    """

    :param numero: Número(id) da palavra a ser buscada
    :return: Indice da palavra caso existe; Se não, retornara -1;
    """
    for i in range(len(frase.palavras)):
        if (frase.palavras[i].numero == numero):
            return i
    return -1
