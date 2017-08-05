"""
@project ensepro
@since 20/07/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import configuracoes

tipos = []
for tipo in configuracoes.getTipoFrases():
    tipos.append((tipo, configuracoes.getTipoFrases()[tipo]))

#TODO FIXME tem problema.
# Está sendo encontrado o tipo corretamente, porém, como a frase é montada de tras para frete, se tem um problema.
# No caso do tipo "quem_sao", somente é validade este tipo quando a palavra "quem" é contatenada ao trechoVerificado, logo
# retorando o numero da palavra "quem" e não da palavra "são" que também faz parte do tipo.
# Também no caso do "quem sao", a ordem que os tipos estão na lista interfere, pois ambos "quem" e "quem são" estarão no trecho validado.
def getTipoFrase(frase):
    """
    Obtem o tipo de uma frase. Caso o tipo não for determinado, o retorno será None.
    :param frase:
    :return:
    """
    palavras = frase.obterPalavrasComPalavraOriginalNaoVazia()
    textoFrase = ""
    for palavra in reversed(palavras):
        textoFrase = palavra.palavraOriginal + " " + textoFrase
        tipo = buscarTipo(textoFrase)
        if(tipo is not None):
            return {
                    "numero_palavra": palavra.numero -5,
                    "tipo": tipo
                   }
    return None




#TODO FIXME pensar em uma estrutura mais otimizada para determinar o tipo. for(for()) não é legal.
# Neste momento foi feito assim(pensando em funcionar) pois este trecho pode não servir mais tarde devido a verificação que será mais complexa.
def buscarTipo(trechoFrase: str) -> str:
    """
    Verifica se o inicio da frase(trechoFrase) está relacionado a algum dos tipos configurados.
    :param trechoFrase:
    :return:
    """
    trechoFrase = trechoFrase.lower()
    for tipo in tipos:
        for valorTipo in tipo[1]:
            if (valorTipo in trechoFrase):
                return tipo[0]
    return None
