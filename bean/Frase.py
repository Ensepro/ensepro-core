"""
@project ensepro
@since 02/08/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import tipofrases
from utils import FraseUtil
from utils import StringUtil
from constantes.TipoFrasesConstantes import NUMERO_PALAVRA
from constantes.FraseConstantes import *
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
        Retorna uma lista com as palavras relevantes da frase.
        :return:
        """
        if (self._palavrasRelevantes is None):
            self._obterPalavrasRelevantes()
        return self._palavrasRelevantes

    def _obterPalavrasRelevantes(self):
        """
        Cria a lista de palavras relevantes
        """

        # Remove palavras que não devem ser consideradas relevantes
        self._palavrasRelevantes = [palavra for palavra in self.palavras if self._isPalavraRelevante(palavra)]

    def _isPalavraRelevante(self, palavra):
        """
        Verifica se a palavra é uma palavra relevante ou não.
        :param palavra: Palavra a ser verificada.
        :return: True ou False
        """

        # 1. Palavras que possuem palavraOriginal vazia.
        if StringUtil.isEmpty(palavra.palavraOriginal):
            return False

        # 2. Palavras não deve fazer parte do tipo da frase
        if palavra.numero <= self.obterTipoFrase()[NUMERO_PALAVRA]:
            return False

        # 3. tagInicial da palavra deve bater com a regex de palavras relevantes
        if not StringUtil.regexExistIn(REGEX_PALAVRA_RELEVANTE, palavra.tagInicial):
            return False

        # 4. Quando a frase estiver a voz passiva, o verbo 'ser' deve ser ignorado.
        if not self.isVozAtiva():
            if palavra.palavraCanonica == "ser":
                return False

        # 5. Quando houver locução verbal, o(s) verbo(s) auxiliar(es) deve ser desconsiderado.
        # O verbo relevante SEMPRE será o último.
        if self.possuiLocucaoVerbal()[LOCUCAO_VERBAL_POSSUI]:
            if (palavra in self.possuiLocucaoVerbal()[LOCUCAO_VERBAL_VERBOS][:-1]):
                return False

        return True

    def possuiLocucaoVerbal(self):
        """
        Verifica se a frase possui locução verbal.
        :return:
        """
        if (self._possuiLocucaoVerbal is None):
            self._verificarLocucaoVerbal()
        return self._possuiLocucaoVerbal

    def _verificarLocucaoVerbal(self):
        """
        Verifica se existe locução verbal, se existir, cria uma lista com os verbos da locução verbal.
        :return:
        """
        verbos = set()
        size = len(self.obterPalavrasComPalavraOriginalNaoVazia()) - 1
        self._possuiLocucaoVerbal = {LOCUCAO_VERBAL_POSSUI: False}

        for i in range(size):
            if self.obterPalavrasComPalavraOriginalNaoVazia()[i].isVerbo() and self.obterPalavrasComPalavraOriginalNaoVazia()[i+1].isVerbo():
                verbos.add(self.obterPalavrasComPalavraOriginalNaoVazia()[i])
                verbos.add(self.obterPalavrasComPalavraOriginalNaoVazia()[i+1])

        if len(verbos) > 0:
            self._possuiLocucaoVerbal = {
                                            LOCUCAO_VERBAL_POSSUI: True,
                                            LOCUCAO_VERBAL_VERBOS: list(verbos)
                                        }

    def isVozAtiva(self):
        """
        Verifica se a frase está na voz ATIVA ou PASSIVA.
        :return:
        """
        if (self._vozAtiva is None):
            self._isVozAtiva()
        return self._vozAtiva

    def _isVozAtiva(self):
        """
        Se existir uma tagInicial que tem o padrão da REGEX_VOZ_PASSIVA então a frase está na voz passiva.
        :return:
        """
        self._vozAtiva = len([palavra for palavra in self.palavras if StringUtil.regexExistIn(REGEX_VOZ_PASSIVA, palavra.tagInicial)]) == 0

    def obterPalavrasComPalavraOriginalNaoVazia(self):
        """
        Este método irá retornar somente as palavras que possuem PALAVRA ORIGINAL não vazia.
        :param frase:
        :return:
        """
        if (self._palavrasComPalavraOriginalNaoVazia is None):
            self._obterPalavrasComPalavraOriginalNaoVazia()
        return self._palavrasComPalavraOriginalNaoVazia

    def _obterPalavrasComPalavraOriginalNaoVazia(self):
        self._palavrasComPalavraOriginalNaoVazia = FraseUtil.removePalavrasSemPalavraOriginal(self.palavras)

    def isQuestao(self):
        """
        Retorna se a frase é uma questão ou não.
        :return: True ou False
        """
        return self.palavras[INDICE_VALIDA_QUESTAO].tagInicial.startswith("QUE")

    def to_json(self):
        return self.__dict__

    @classmethod
    def fraseFromJson(cls, jsonFrase):
        palavras = FraseUtil.palavrasFromJson(jsonFrase)
        return cls(palavras)
