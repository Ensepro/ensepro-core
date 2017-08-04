"""
@project ensepro
@since 02/08/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import sys

from utils import StringUtil
from utils import WordNetUtil as wn


class Palavra(object):

    def __init__(self, numero):
        self.numero = numero
        self.nivel = 0
        self.palavraOriginal = ""
        self.palavraCanonica = ""
        self.tags = []
        self.tagInicial = ""
        self.sinonimos = None


    def getSinonimos(self):
        if (self.sinonimos is not None):
            return self.sinonimos if len(self.sinonimos) > 0 else None

        self.sinonimos["eng"] = wn.getSinonimos(self.palavraCanonica, "eng")
        self.sinonimos["por"] = wn.getSinonimos(self.palavraCanonica, "por")

        return self.getSinonimos()


    def print(self):
        print(self.numero)
        print(self.nivel)
        print(self.palavraOriginal)
        print(self.palavraCanonica)
        print(self.tags)
        print(self.tagInicial)
        print(self.sinonimos)

    def __hash__(self):
        return self.numero

    def __eq__(self, other):
        # TODO numero somente? ou palavra também?
        return self.numero == other.numero  # and self.palavraOriginal == other.palavraOriginal;