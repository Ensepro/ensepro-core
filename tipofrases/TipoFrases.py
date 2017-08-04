"""
@project ensepro
@since 20/07/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from bean import Frase
from utils import StringUtil
import configuracoes


tipos = []
for tipo in configuracoes.getTipoFrases():
    tipos.append((tipo, configuracoes.getTipoFrases()[tipo]))

#TODO FIXME tem problema.
# "QUEM É BLALA" ele está achando o tipo "quem" e deveria ser "quem_sao". Ele pega a primeira palavra e procura o tipo.
def getTipoFrase(frase : Frase):
    """
    Obtem o tipo de uma frase. Caso o tipo não for determinado, o retorno será None.
    :param frase:
    :return:
    """
    palavras = getPalavrasDaFrase(frase)
    textoFrase = palavras[0].palavraOriginal
    palavras.pop(0)
    for palavra in palavras:
        tipo = buscarTipo(textoFrase)
        if(tipo is not None):
            return (palavra.numero, tipo)
        textoFrase = textoFrase + " " + palavra.palavraOriginal

    return None


def buscarTipo(trechoFrase: str) -> str:
    """
    Verifica se o inicio da frase(trechoFrase) está relacionado a algum dos tipos configurados.
    :param trechoFrase:
    :return:
    """
    # print("buscarTipo:'"+trechoFrase+"'")
    trechoFrase = trechoFrase.lower()
    for tipo in tipos:
        if (trechoFrase in tipo[1]):
            return tipo[0]
    return None


def getPalavrasDaFrase(frase : Frase):
    """
    Este método irá remover as palavras que não possuem a palavra original na frase.
    :param frase:
    :return:
    """
    return [palavra for palavra in frase.palavras if not StringUtil.isEmpty(palavra.palavraOriginal)]
