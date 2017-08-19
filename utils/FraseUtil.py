"""
@project ensepro
@since 19/07/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
from bean.Palavra import Palavra
from utils import StringUtil
from .StringUtil import isEmpty


def palavrasFromJson(jsonFrase):
    """
    Retorna uma lista de palavras a partir de um objeto json.
    :param jsonFrase: Json que encapsula a lista de palavras de uma frase.
    :return:
    """
    palavras = []
    for palavra in jsonFrase:
        palavras.append(Palavra(palavra))
    return palavras


def obterPalavrasComTagInicialMatchingAnyRegex(frase, tagsRegex: list):
    """
    Este método irá verificar se as tags inicias das palavras da frase batem com algum dos regex passados por parâmetro.
    :param frase: é o objeto Frase do qual as palavras serão filtradas.
    :param tagsRegex: Lista de regexs que serão utilizadas para validar a tagInicial das palavras.
    :return: Lista de palavras que a sua tagInicial foi validada por alguma regex
    """
    palavrasResultantes = []
    for palavra in frase.palavras:
        for tagRegex in tagsRegex:
            if StringUtil.regexExistIn(tagRegex, palavra.tagInicial):
                palavrasResultantes.append(palavra)
                break

    return palavrasResultantes


def removePalavrasSemPalavraOriginal(palavras: list):
    return [palavra for palavra in palavras if not isEmpty(palavra.palavraOriginal)]
