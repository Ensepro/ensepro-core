# -*- coding: utf-8 -*-
"""
@project ensepro
@since 25/02/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from nltk.tree import Tree
from ensepro.constantes import LoggerConstantes

logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_ARVORE)


class Arvore:

    def __init__(self):
        self.__nodes = {}

    @property
    def nodes(self):
        return self.__nodes

    @property
    def roots(self):
        """
        A(s) raiz(es) da árvore são os nodes que não possuem pais.
        :return: Todos os nodos que são raizes.
        """
        return [node for node in self.nodes.values() if not node.pai]

    def adicionar_node(self, id, value, id_pai=None):
        logger.debug("Adicionando node: [id=%s, value=%s, id_pai=%s]", id, value, id_pai)
        node = Node(id, value)

        if id_pai:
            pai = self[id_pai]
            node = Node(id, value, pai)
            pai.adicionar_filho(node)

        self[id] = node
        return node

    def to_nltk_tree(self, brackets="[]") -> Tree:
        return Tree.fromstring(str(self), brackets=brackets, remove_empty_top_bracketing=True)

    def __getitem__(self, key):
        return self.__nodes[key]

    def __setitem__(self, key, item):
        self.__nodes[key] = item

    def __str__(self):
        to_string = ""
        for node in self.roots:
            to_string += str(node)

        return "[ {}]".format(to_string)


class Node:
    def __init__(self, id, value, pai=None):
        self.__id = id
        self.__valor = value
        self.__pai = pai
        self.__nivel = (pai.nivel + 1) if pai else 0
        self.__filhos = []

    @property
    def id(self):
        return self.__id

    @property
    def valor(self):
        return self.__valor

    @property
    def nivel(self):
        return self.__nivel

    @property
    def pai(self):
        return self.__pai

    @property
    def filhos(self):
        return self.__filhos

    @property
    def is_terminal(self):
        # se não possui filhos, é terminal/folha
        return not bool(self.__filhos)

    @property
    def is_nao_terminal(self):
        # se possui filhos, não é terminal/folha
        return bool(self.__filhos)

    def adicionar_filho(self, node):
        logger.debug("Adicionando filho: [pai=%s, filho=%s]", self.id, node)
        self.__filhos.append(node)

    def __str_filhos(self):
        str_filhos = ""
        for filho in self.__filhos:
            str_filhos += str(filho)

        return str_filhos

    def __str__(self):
        str_this = str(self.__valor)
        if (self.is_terminal):
            return "{} ".format(str_this)

        str_filhos = self.__str_filhos()
        return "[ {0} {1}] ".format(str_this, str_filhos)
