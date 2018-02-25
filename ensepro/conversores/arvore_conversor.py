# -*- coding: utf-8 -*-
"""
@project ensepro
@since 25/02/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
from ensepro.arvore import Arvore


def __corrige_problema_ordenacao_arvore_printada(palavra):
    """
    Este problema ocorre quando a palavra não possui uma palavra_original e não possui filhos,
    como no exemplo das sub-arvores (ex:X:par|2|, também não possui palavra_original, mas possui filhos).

    Quando uma palavra não possui palavra_original, o termo se torna uma folha, e o print feito
    pela nltk.tree.Tree faz algum tipo de ordenação e printa primeiro as folhas, e depois as sub-arvores.

    Frase usada para exemplo: "Alencar, tudo bem?"
    Sem correção: ---------------------------------------------------------------
                               UTT:x|1|
                       ___________|____________
                   X:par|2|
              ________|___________         ____|______
             |   CJT:prop|3| CJT:spec|5|  |       fA:adv|6|
             |        |           |       |           |
            ,|4|   Alencar       tudo    ?|7|        bem

    Com correção: ---------------------------------------------------------------
                               UTT:x|1|
                        __________|_________________
                    X:par|2|
              _________|__________            ______|___
        CJT:prop|3|   ,|4|   CJT:spec|5| fA:adv|6|     ?|7|
             |         |          |          |          |
          Alencar     ...        tudo       bem        ...
    """
    if palavra.palavra_original:
        return

    CARACTERES_PARA_ADICIONAR_ESPACO = ",.;:?!\"()`'"

    if palavra.tag_inicial in CARACTERES_PARA_ADICIONAR_ESPACO:
        palavra.palavra_original = ' '


def from_frase(frase):
    arvore = Arvore()
    ultimo_node_adicionado = None
    index = 0
    numero_de_palavras = len(frase.palavras)

    # Enquando não percorreu todas as palavras da frase, continua
    while (index < numero_de_palavras):
        palavra = frase.palavras[index]

        # Quando ocorre algum palavra sem palavra_original e com tag_inicial, a ordem de aparição na arvore printada
        # pelo nltk.tree.Tree fica errada, sendo esta palavra printada antes das demais.
        # O método abaixo corrige este problema e informa uma melhor explicação
        __corrige_problema_ordenacao_arvore_printada(palavra)

        # Se possui um último node adicionado, indica que a palavra atual pode ser filho deste node
        if ultimo_node_adicionado:
            # se a palavra atual tiver um nivel maior que o node anterior, indica que é filho dele
            if ultimo_node_adicionado.valor.nivel < palavra.nivel:
                ultimo_node_adicionado = arvore.adicionar_node(palavra.id, palavra, ultimo_node_adicionado.id)
                index += 1
            # se não for filho do último node, verifica se é irmão dele(ou seja, filho do pai do último node)
            # para isto, o último node passa a ser o pai do último node atual e o index não é incrementado
            else:
                if ultimo_node_adicionado.pai:
                    ultimo_node_adicionado = ultimo_node_adicionado.pai
                # se o último node não possuir um pai, indica que ele é uma raiz, logo, o próximo nodo também será
                else:
                    ultimo_node_adicionado = None
        # se o último node adicionado é None, então está palavra é uma raiz
        else:
            ultimo_node_adicionado = arvore.adicionar_node(palavra.id, palavra)
            index += 1

    return arvore
