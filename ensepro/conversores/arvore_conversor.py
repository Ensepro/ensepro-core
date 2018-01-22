"""
@project ensepro
@since 21/01/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
from ensepro.arvore import Arvore


def from_frase(frase):
    arvore = Arvore()
    limpar_ultima_palavra = False
    ultimo_node_adicionado = None
    index = 0
    numero_de_palavras = len(frase.palavras)

    # Enquando não percorreu todas as palavras da frase, continua
    while (index < numero_de_palavras):
        palavra = frase.palavras[index]

        if (index + 1) == numero_de_palavras \
                and palavra.tag_inicial \
                and not palavra.palavra_original:
            # Se a última palavra somente possuir tag_inicial(e tiver a palavra_original vazia), a árvore gerada pelo nltk.tree.Tree
            # coloca o nó dessa última palavra na primeira subarvore, antes das demais palavras.
            # A solução é colocar a palavra_original com um espaço
            palavra.palavra_original = " "
            limpar_ultima_palavra = True

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

    # Comentado pois como o objeto é o mesmo, se a árvore for printada novamente depois, não terá mais o espaço para corrigir
    # 
    # if limpar_ultima_palavra:
    #     # Caso foi adicionado um espaço na palavra_original da última palavra, é feito sua remoção antes de seguir
    #     frase.palavras[numero_de_palavras - 1].palavra_original = ''

    return arvore
