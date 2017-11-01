"""
@project ensepro
@since 02/08/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import tipofrases
from utils import FraseUtil
from utils.FraseUtil import get_dn, get_nucluo
from utils.FraseTreeUtil import get_sub_tree, get_up_tree
from utils import StringUtil
from constantes.TipoFrasesConstantes import NUMERO_PALAVRA, TIPO_FRASE
from constantes.FraseConstantes import *
from conversores import MakeJsonSerializable


class Frase(object):

    def __init__(self, *args, **kwargs):
        self.palavras = args[0]
        self.id = args[1]
        self.__palavrasComPalavraOriginalNaoVazia = None
        self.__tipo = None
        self.__palavrasRelevantes = None
        self.__possuiLocucaoVerbal = None
        self.__vozAtiva = None
        self.__adjuntos_complementos = None

    def obterTipoFrase(self):
        if (self.__tipo is None):
            self.__obterTipoFrase()
        return self.__tipo

    def __obterTipoFrase(self):
        self.__tipo = tipofrases.getTipoFrase(self)

    def obterPalavrasRelevantes(self):
        """
        Retorna uma lista com as palavras relevantes da frase.
        :return:
        """
        if (self.__palavrasRelevantes is None):
            self.__obterPalavrasRelevantes()
        return self.__palavrasRelevantes

    def __obterPalavrasRelevantes(self):
        """
        Cria a lista de palavras relevantes
        """

        # Remove palavras que não devem ser consideradas relevantes
        self.__palavrasRelevantes = [palavra for palavra in self.palavras if self.__isPalavraRelevante(palavra)]

    def __isPalavraRelevante(self, palavra):
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
        if (self.__possuiLocucaoVerbal is None):
            self.__verificarLocucaoVerbal()
        return self.__possuiLocucaoVerbal

    def __verificarLocucaoVerbal(self):
        """
        Verifica se existe locução verbal, se existir, cria uma lista com os verbos da locução verbal.
        :return:
        """
        verbos = set()
        size = len(self.obterPalavrasComPalavraOriginalNaoVazia()) - 1
        self.__possuiLocucaoVerbal = {LOCUCAO_VERBAL_POSSUI: False}

        for i in range(size):
            if self.obterPalavrasComPalavraOriginalNaoVazia()[i].isVerbo() and self.obterPalavrasComPalavraOriginalNaoVazia()[i+1].isVerbo():
                verbos.add(self.obterPalavrasComPalavraOriginalNaoVazia()[i])
                verbos.add(self.obterPalavrasComPalavraOriginalNaoVazia()[i+1])

        if len(verbos) > 0:
            self.__possuiLocucaoVerbal = {
                                            LOCUCAO_VERBAL_POSSUI: True,
                                            LOCUCAO_VERBAL_VERBOS: list(verbos)
                                        }

    def isVozAtiva(self):
        """
        Verifica se a frase está na voz ATIVA ou PASSIVA.
        :return:
        """
        if (self.__vozAtiva is None):
            self.__isVozAtiva()
        return self.__vozAtiva

    def __isVozAtiva(self):
        """
        Se existir uma tagInicial que tem o padrão da REGEX_VOZ_PASSIVA então a frase está na voz passiva.
        :return:
        """
        self.__vozAtiva = len([palavra for palavra in self.palavras if StringUtil.regexExistIn(REGEX_VOZ_PASSIVA, palavra.tagInicial)]) == 0

    def obterPalavrasComPalavraOriginalNaoVazia(self):
        """
        Este método irá retornar somente as palavras que possuem PALAVRA ORIGINAL não vazia.
        :param frase:
        :return:
        """
        if (self.__palavrasComPalavraOriginalNaoVazia is None):
            self.__obterPalavrasComPalavraOriginalNaoVazia()
        return self.__palavrasComPalavraOriginalNaoVazia

    def __obterPalavrasComPalavraOriginalNaoVazia(self):
        self.__palavrasComPalavraOriginalNaoVazia = FraseUtil.removePalavrasSemPalavraOriginal(self.palavras)


    def getAdjuntosComplementos(self):
        if self.__adjuntos_complementos is None:
            self.__adjuntos_complementos = []
            self.__getAdjuntosComplementos(self)

        return self.__adjuntos_complementos

    def __getAdjuntosComplementos(self, frase):
        dn = get_dn(frase)
        if not dn:
            return
        nivel_superior = get_up_tree(frase, dn)

        if not nivel_superior:
            return

        nivel_superior_tree = get_sub_tree(frase, nivel_superior)
        frase_nivel_superior = Frase(nivel_superior_tree, frase.id)

        if not frase_nivel_superior:
            return

        nivel_dn_tree = get_sub_tree(frase, dn)
        frase_nivel_dn = Frase(nivel_dn_tree, frase.id)

        if not frase_nivel_dn:
            return

        adjunto = get_nucluo(frase_nivel_superior)
        complemento = get_nucluo(frase_nivel_dn)

        self.__adjuntos_complementos.append({
            "nome": adjunto,
            "complemento": complemento
        })

        self.__getAdjuntosComplementos(frase_nivel_dn)


    def isQuestao(self):
        """
        Retorna se a frase é uma questão ou não.
        :return: True ou False
        """
        return self.palavras[INDICE_VALIDA_QUESTAO].tagInicial.startswith("QUE")

    def isConsulta(self):
        if self.obterTipoFrase():
            return self.obterTipoFrase()[TIPO_FRASE] == "consulta"
        return False

    def to_json(self):
        return self.__dict__

    @classmethod
    def fraseFromJson(cls, jsonFrase, fraseId):
        palavras = FraseUtil.palavrasFromJson(jsonFrase)
        return cls(palavras, fraseId)
