"""
@project ensepro
@since 20/07/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import configuracoes
from constantes.TipoFrasesConstantes import *

def getTipoFrase(frase):
    """
    Obtém o tipo de uma frase. Caso o tipo não for determinado, o retorno será None.
    :param frase:
    :return:
    """
    palavras = frase.obterPalavrasComPalavraOriginalNaoVazia()
    tipo = _tipos

    for i in range(len(palavras)):
        if palavras[i].palavraCanonica in tipo:
            tipo = tipo[palavras[i].palavraCanonica]
            continue

        return {
                NUMERO_PALAVRA: palavras[i - 1].numero if TIPO_KEY in tipo else -1,
                TIPO_FRASE: tipo[TIPO_KEY] if TIPO_KEY in tipo else None
        }


_tipos = configuracoes.getTipoFrases()
