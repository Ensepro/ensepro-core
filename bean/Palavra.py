"""
@project ensepro
@since 02/08/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from constantes.FraseConstantes import REGEX_PALAVRA_VERBO
from conversores import MakeJsonSerializable
from utils import WordNetUtil as wn
from utils import StringUtil


class Palavra(object):
    def __init__(self, *args, **kwargs):
        palavra = args[0]
        self.numero = palavra["numero"]
        self.nivel = palavra["nivel"]
        self.palavraOriginal = palavra["palavraOriginal"].lower()
        self.palavraCanonica = palavra["palavraCanonica"].lower()
        self.tags = palavra["tags"]
        self.tagInicial = palavra["tagInicial"]
        self.sinonimos = None

    def getSinonimos(self):
        """
        Obtém os sinônimos da palavra.
        :return:
        """
        if (self.sinonimos is not None):
            return self.sinonimos if len(self.sinonimos) > 0 else None

        self.sinonimos = {}
        self.sinonimos["eng"] = wn.getSinonimos(self.palavraCanonica, "eng")
        self.sinonimos["por"] = wn.getSinonimos(self.palavraCanonica, "por")

        return self.getSinonimos()


    def isVerbo(self):
        """
        Retorna se a frase é um verbo ou não.
        :return:
        """
        return StringUtil.regexExistIn(REGEX_PALAVRA_VERBO, self.tagInicial)

    def to_json(self):
        return self.__dict__

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "[\"" + self.tagInicial + "\" |> \"" + self.palavraOriginal + "\"]"

    def __hash__(self):
        return self.numero

    def __eq__(self, other):
        return self.numero == other.numero
