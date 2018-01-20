"""
@project ensepro
@since 18/12/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from nltk.tree import Tree


class Arvore:

    def __init__(self):
        self.__nodes = {}

    @property
    def nodes(self):
        return self.__nodes

    def adicionar_node(self, id, value, id_pai=None):
        # TODO: #ADD_LOG
        node = Node(id, value)

        if id_pai:
            pai = self[id_pai]
            node = Node(id, value, pai)
            pai.adicionar_filho(node)

        self[id] = node
        return node

    def to_nltk_tree(self, brackets="[]") -> Tree:
        return Tree.fromstring(str(self), brackets=brackets)

    def __getitem__(self, key):
        return self.__nodes[key]

    def __setitem__(self, key, item):
        self.__nodes[key] = item

    def __str__(self):
        to_string = ""
        for node in self.__nodes.values():
            if (not node.pai):
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
        return not self.__filhos

    def adicionar_filho(self, node):
        self.__filhos.append(node)

    def __str_filhos(self):
        str_filhos = ""
        for filho in self.__filhos:
            str_filhos += str(filho)

        return str_filhos

    def __str__(self):
        str_pai = str(self.__valor)
        if (self.is_terminal):
            return "{} ".format(str_pai)

        str_filhos = self.__str_filhos()
        return "[ {0} {1}] ".format(str_pai, str_filhos)
