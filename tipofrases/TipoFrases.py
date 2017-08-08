"""
@project ensepro
@since 20/07/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import configuracoes

tipos = configuracoes.getTipoFrases()

def getTipoFrase(frase):
    """
    Obtem o tipo de uma frase. Caso o tipo não for determinado, o retorno será None.
    :param frase:
    :return:
    """
    palavras = frase.obterPalavrasComPalavraOriginalNaoVazia()
    tipo = tipos

    for i in range(len(palavras)):
        if palavras[i].palavraOriginal in tipo:
            tipo = tipo[palavras[i].palavraOriginal]
            continue

        return {
                "numero_palavra": palavras[i-1].numero,
                "tipo": tipo["tipo"]
               }





