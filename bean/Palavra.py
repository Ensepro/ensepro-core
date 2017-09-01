"""
@project ensepro
@since 02/08/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from constantes.FraseConstantes import REGEX_PALAVRA_VERBO
from constantes.FraseConstantes import REGEX_PALAVRA_ADJETIVO
from constantes.FraseConstantes import REGEX_PALAVRA_PREPOSICAO
from constantes.FraseConstantes import REGEX_PALAVRA_SUBSTANTIVO
from conversores import MakeJsonSerializable
from utils import WordNetUtil as wn
from utils import StringUtil
from utils import SinonimoUtil
from utils import PalavraUtil
import configuracoes


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

        _sinonimos = {}

        sinonimosLinguagens = configuracoes.getSinonimosLinguagens()
        for lang in sinonimosLinguagens:
            _sinonimos[lang] = wn.getSinonimos(self.palavraCanonica, lang)

        self.criarSinonimosObjetos(_sinonimos)

        return self.sinonimos

    def criarSinonimosObjetos(self, _sinonimos):
        self.sinonimos = {}
        numero = 1
        for lang in _sinonimos:
            self.sinonimos[lang] = []
            for _sinonimo in _sinonimos[lang]:
                sinonimoTemp = SinonimoUtil.stringToSinonimo(_sinonimo, numero)

                isMesmaClasseGramatical = PalavraUtil.isMesmaClasseGramatical(self, sinonimoTemp)
                naoExiste = sinonimoTemp not in self.sinonimos[lang]
                diferenteDaPalavra = sinonimoTemp.sinonimo != self.palavraCanonica

                if isMesmaClasseGramatical and naoExiste and diferenteDaPalavra:
                    self.sinonimos[lang].append(sinonimoTemp)
                    numero += 1

    def isVerbo(self):
        return StringUtil.regexExistIn(REGEX_PALAVRA_VERBO, self.tagInicial)

    def isAdjetivo(self):
        return StringUtil.regexExistIn(REGEX_PALAVRA_ADJETIVO, self.tagInicial)

    def isSubstantivo(self):
        return StringUtil.regexExistIn(REGEX_PALAVRA_SUBSTANTIVO, self.tagInicial)

    def isPreposicao(self):
        return StringUtil.regexExistIn(REGEX_PALAVRA_PREPOSICAO, self.tagInicial)

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
