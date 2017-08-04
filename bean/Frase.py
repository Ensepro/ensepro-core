"""
@project ensepro
@since 02/08/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from .Palavra import Palavra

class Frase(object):


    def __init__(self):
        self.palavras = []

   # <Métodos considerando lista como árore>
    def _montaArvore(self, nivelAnterior, arvore, lista, i):
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
            return self._montaArvore(thisNivel, arvore, lista, i + 1)

        if (thisNivel == nivelAnterior):
            if ((i + 1) < len(lista) and int(lista[i + 1].nivel) > thisNivel):
                arvore = arvore + " (" + lista[i].tagInicial + "|" + str(lista[i].numero) + "| " + lista[i].palavraOriginal + ""
            else:
                arvore = arvore + " (" + lista[i].tagInicial + "|" + str(lista[i].numero) + "| " + lista[i].palavraOriginal + ")"
            return self._montaArvore(thisNivel, arvore, lista, i + 1)

        if (thisNivel < nivelAnterior):
            arvore = arvore + (")" * (nivelAnterior - thisNivel))
            return self._montaArvore(thisNivel, arvore, lista, i)

    # </Métodos considerando lista como árore>