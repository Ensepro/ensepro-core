"""
@project ensepro
@since 02/08/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from conversores import MakeJsonSerializable
from utils import WordNetUtil as wn

class Palavra(object):

    def __init__(self, *args, **kwargs):
        palavra = args[0]
        self.numero = palavra["numero"]
        self.nivel = palavra["nivel"]
        self.palavraOriginal = palavra["palavraOriginal"]
        self.palavraCanonica = palavra["palavraCanonica"]
        self.tags = palavra["tags"]
        self.tagInicial = palavra["tagInicial"]
        self.sinonimos = None


    def getSinonimos(self):
        if (self.sinonimos is not None):
            return self.sinonimos if len(self.sinonimos) > 0 else None

        self.sinonimos = {}
        self.sinonimos["eng"] = wn.getSinonimos(self.palavraCanonica, "eng")
        self.sinonimos["por"] = wn.getSinonimos(self.palavraCanonica, "por")

        # print(self.sinonimos)
        return self.getSinonimos()



    def print(self):
        print(self.numero)
        print(self.nivel)
        print(self.palavraOriginal)
        print(self.palavraCanonica)
        print(self.tags)
        print(self.tagInicial)
        print(self.sinonimos)


    def to_json(self):
        return self.__dict__

    def __hash__(self):
        return self.numero

    def __eq__(self, other):
        return self.numero == other.numero