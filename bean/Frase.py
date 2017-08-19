"""
@project ensepro
@since 02/08/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import tipofrases
import re
from utils import FraseUtil
from utils import StringUtil
from constantes.TipoFrasesConstantes import NUMERO_PALAVRA
from constantes.FraseConstantes import INDICE_VALIDA_QUESTAO
from conversores import MakeJsonSerializable


class Frase(object):
    def __init__(self, *args, **kwargs):
        self.palavras = args[0]
        self._palavrasComPalavraOriginalNaoVazia = None
        self._tipo = None
        self._palavrasRelevantes = None
        self._possuiLocucaoVerbal = None
        self._vozAtiva = None

    def obterTipoFrase(self):
        if (self._tipo is None):
            self._obterTipoFrase()
        return self._tipo

    def _obterTipoFrase(self):
        self._tipo = tipofrases.getTipoFrase(self)

    def obterPalavrasRelevantes(self):
        """
        Obtém as palavras relevantes da frase para esta ser analisada.
        :return:
        """
        if (self._palavrasRelevantes is None):
            self._obterPalavrasRelevantes()
        return self._palavrasRelevantes

    # TODO revisar as regex que são necessárias. Tentar separar o código em trechos menores (se possível)
    # também verificar se não é melhor utilizar somente uma regex com OR's assim evitando um for para percorrer e verificar com cada uma.
    # Ex: v-|^H:n$|^DN:adj$"|^H:prop$|^S:n$|^Cs:n$|^DP:n$|^Cs:prop$|^DP:prop$
    def _obterPalavrasRelevantes(self):
        regexs = [
            re.compile("v-"),
            re.compile("^H:n$"),
            re.compile("^DN:adj$"),
            re.compile("^H:prop$"),
            re.compile("^S:n$"),
            re.compile("^Cs:n$"),
            re.compile("^DP:n$"),
            re.compile("^Cs:prop$"),
            re.compile("^DP:prop$")
        ]

        _palavrasRelevantesTemp = FraseUtil.obterPalavrasComTagInicialMatchingAnyRegex(self, regexs)

        # Remove palavras que não devem ser consideradas relevantes
        self._palavrasRelevantes = [palavra for palavra in _palavrasRelevantesTemp if self._isPalavraRelevante(palavra)]

    def _isPalavraRelevante(self, palavra):
        # 1. Palavras que possuem palavraOriginal vazia.
        if StringUtil.isEmpty(palavra.palavraOriginal):
            return False

        # 2. Palavras não deve fazer parte do tipo da frase
        if palavra.numero <= self.obterTipoFrase()[NUMERO_PALAVRA]:
            return False

        # 3. Quando a frase estiver a voz passiva, o verbo 'ser' deve ser ignorado.
        if not self.isVozAtiva():
            if palavra.palavraCanonica == "ser":
                return False

        # 4. Quando houver locução verbal, o verbo auxiliar deve ser desconsiderado.
        if self.possuiLocucaoVerbal()["possui"]:
            # TODO rever ação
            regexAux = re.compile("aux")
            if StringUtil.regexExistIn(regexAux, palavra.tagInicial):
                return False

        return True

    def possuiLocucaoVerbal(self):
        """
        Verifica se a frase possui locução verbal.
        :return:
        """
        if (self._possuiLocucaoVerbal is None):
            self._possuiLocucaoVerbal_()
        return self._possuiLocucaoVerbal

    # TODO verificar o nome dos atributos "possui", "palavra1" e "palavra2"
    def _possuiLocucaoVerbal_(self):
        regex = re.compile("v-")
        size = len(self.obterPalavrasComPalavraOriginalNaoVazia()) - 1
        self._possuiLocucaoVerbal = {"possui": False}
        for i in range(size):
            if (StringUtil.regexExistIn(regex, self._palavrasComPalavraOriginalNaoVazia[i].tagInicial) and StringUtil.regexExistIn(regex, self._palavrasComPalavraOriginalNaoVazia[i + 1].tagInicial)):
                self._possuiLocucaoVerbal = {"possui": True,
                                             "palavra1": self._palavrasComPalavraOriginalNaoVazia[i],
                                             "palavra2": self._palavrasComPalavraOriginalNaoVazia[i + 1]
                                             }
                break

    def isVozAtiva(self):
        """
        Verifica se a frase está na voz ATIVA ou PASSIVA.
        :return:
        """
        if (self._vozAtiva is None):
            self._isVozAtiva()
        return self._vozAtiva

    def _isVozAtiva(self):
        regex = [re.compile("^fApass:pp$")]
        self._vozAtiva = len(FraseUtil.obterPalavrasComTagInicialMatchingAnyRegex(self, regex)) == 0


        # <Métodos considerando lista como árore>

    def obterPalavrasComPalavraOriginalNaoVazia(self):
        """
        Este método irá retornar somente as palavras que possuem PALAVRA ORIGINAL.
        :param frase:
        :return:
        """
        if (self._palavrasComPalavraOriginalNaoVazia is None):
            self._obterPalavrasComPalavraOriginalNaoVazia()
        return self._palavrasComPalavraOriginalNaoVazia

    def _obterPalavrasComPalavraOriginalNaoVazia(self):
        self._palavrasComPalavraOriginalNaoVazia = FraseUtil.removePalavrasSemPalavraOriginal(self.palavras)

    def isQuestao(self):
        return self.palavras[INDICE_VALIDA_QUESTAO].tagInicial.startswith("QUE")

    def to_json(self):
        return self.__dict__

    @classmethod
    def fraseFromJson(cls, jsonFrase):
        palavras = FraseUtil.palavrasFromJson(jsonFrase)
        return cls(palavras)
