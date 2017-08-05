"""
@project ensepro
@since 19/07/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
from bean.Palavra import Palavra

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


def obterPalavrasComTagInicialMatchingAnyRegex(frase, tagsRegex : list):
    """
    Este método irá verificar se as tags inicias das palavras da frase batem com os regex passados.
    :param frase: é o objeto Frase do qual as palavras serão filtradas.
    :param tagsRegex: Lista de regexs que serão utilizadas para validar a tagInicial das palavras.
    :return: Lista de palavras que a sua tagInicial foi validada por alguma regex
    """
    palavrasResultantes = []
    palavras = frase.obterPalavrasComPalavraOriginalNaoVazia()

    #FIXME: verificar uma maneira de não fazer o FOR abaixo
    #Obtem todas as palavras após as quais determinam o tipo, pois estas só são relevantes para verificar o tipo
    # e não serão mais necessárias para a análise.
    palavras = [palavra for palavra in palavras if palavra.numero > frase.obterTipoFrase()["numero_palavra"]]

    for palavra in palavras:
        for tagRegex in tagsRegex:
            if(tagRegex.search(palavra.tagInicial) is not None):
                palavrasResultantes.append(palavra)
                break

    return palavrasResultantes



