"""
@project ensepro
@since 02/08/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import tipofrases
import re
from utils import FraseUtil
from utils import StringUtil
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
        if(self._tipo is None):
            self._obterTipoFrase()
        return self._tipo

    def _obterTipoFrase(self):
        self._tipo = tipofrases.getTipoFrase(self)


    def obterPalavrasRelevantes(self):
        """
        Obtém as palavras relevantes da frase para esta ser analisada.
        :return:
        """
        if(self._palavrasRelevantes is None):
            self._obterPalavrasRelevantes()
        return self._palavrasRelevantes

    # TODO revisar as regex que são necessárias
    # também verificar se não é melhor utilizar somente uma regex com OR'sm assim evitando um for para percorrer e verificar com cada uma.
    # Ex: v-|^H:n$|^DN:adj$"|^H:prop$|^S:n$|^Cs:n$|^DP:n$
    def _obterPalavrasRelevantes(self):
        self._palavrasRelevantes = FraseUtil.obterPalavrasComTagInicialMatchingAnyRegex(self,
                                    [
                                        re.compile("v-"),
                                        re.compile("^H:n$"),
                                        re.compile("^DN:adj$"),
                                        re.compile("^H:prop$"),
                                        re.compile("^S:n$"),
                                        re.compile("^Cs:n$"),
                                        re.compile("^DP:n$")
                                    ])


    def possuiLocucaoVerbal(self):
        """
        Verifica se a frase possui locução verbal.
        :return:
        """
        if(self._possuiLocucaoVerbal is None):
            self._possuiLocucaoVerbal_()
        return self._possuiLocucaoVerbal

    def _possuiLocucaoVerbal_(self):
        regex = re.compile("v-")
        size = len(self.obterPalavrasRelevantes()) - 1
        for i in range(size):
            if(regex.search(self._palavrasRelevantes[i].tagInicial) is not None and regex.search(self._palavrasRelevantes[i+1].tagInicial) is not None):
                self._possuiLocucaoVerbal = {"possui": True, "palavra1": self._palavrasRelevantes[i], "palavra2": self._palavrasRelevantes[i+1]}


    def isVozAtiva(self):
        """
        Verifica se a frase está na voz ATIVA ou PASSIVA.
        :return:
        """
        if (self._vozAtiva is None):
            self._isVozAtiva()
        return self._vozAtiva

    def _isVozAtiva(self):
        regex = [ re.compile("^fApass:pp$") ]
        self._vozAtiva = len(FraseUtil.obterPalavrasComTagInicialMatchingAnyRegex(self, regex)) > 0


   # <Métodos considerando lista como árore>


    def obterPalavrasComPalavraOriginalNaoVazia(self):
        """
        Este método irá retornar somente as palavras que possuem PALAVRA ORIGINAL.
        :param frase:
        :return:
        """
        if(self._palavrasComPalavraOriginalNaoVazia is None):
            self._obterPalavrasComPalavraOriginalNaoVazia()
        return self._palavrasComPalavraOriginalNaoVazia

    def _obterPalavrasComPalavraOriginalNaoVazia(self):
        self._palavrasComPalavraOriginalNaoVazia = [palavra for palavra in self.palavras if not StringUtil.isEmpty(palavra.palavraOriginal)]

    def to_json(self):
        return self.__dict__

    @classmethod
    def fraseFromJson(cls, jsonFrase):
        palavras = FraseUtil.palavrasFromJson(jsonFrase)
        return cls(palavras)

