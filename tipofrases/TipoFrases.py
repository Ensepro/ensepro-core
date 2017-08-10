"""
@project ensepro
@since 20/07/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import configuracoes
from constantes.TipoFrasesConstantes import *


# TODO
def _normalizarTipos():
    """

    :param tipos:
    :return:
    """
    pass


def getTipoFrase(frase):
    """
    Obtém o tipo de uma frase. Caso o tipo não for determinado, o retorno será None.
    :param frase:
    :return:
    """
    palavras = frase.obterPalavrasComPalavraOriginalNaoVazia()
    tipo = _tipos

    for i in range(len(palavras)):
        if palavras[i].palavraOriginal in tipo:
            tipo = tipo[palavras[i].palavraOriginal]
            continue

        return {NUMERO_PALAVRA: palavras[i - 1].numero, TIPO_PALAVRA: tipo["tipo"]
                }


_tipos = configuracoes.getTipoFrases()
_normalizarTipos()
