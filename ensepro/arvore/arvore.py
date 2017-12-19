"""
@project ensepro
@since 18/12/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""


class Arvore:

    def __init__(self):
        self.__nodes = {}

    @property
    def nodes(self):
        return self.__nodes

    def adicionar_node(self, id, value, id_pai=None):
        node = Node(id, value)

        if id_pai:
            pai = self[id_pai]
            node = Node(id, value, pai)
            pai.adicionar_filho(node)

        self[id] = node
        return node

    def __getitem__(self, key):
        return self.__nodes[key]

    def __setitem__(self, key, item):
        self.__nodes[key] = item

    def __str__(self):
        to_string = ""
        for node in self.__nodes.values():
            if(not node.pai):
                to_string += str(node)

        return "( {})".format(to_string)


class Node:
    def __init__(self, id, value, pai=None):
        self.__id = id
        self.__valor = value
        self.__pai = pai
        self.__nivel = pai.nivel if pai else 0
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
        return "( {0} {1}) ".format(str_pai, str_filhos)


"""
(_ROOT, _DEPTH, _BREADTH) = range(3)

class Tree:
    def __init__(self):
        self.__nodes = {}

    @property
    def nodes(self):
        return self.__nodes

    def add_node(self, identifier, parent=None):
        node = Node(identifier)
        self[identifier] = node

        if parent is not None:
            self[parent].add_child(identifier)

        return node

    def display(self, identifier, depth=_ROOT):
        children = self[identifier].children
        if depth == _ROOT:
            print("{0}".format(identifier))
        else:
            print("\t" * depth, "{0}".format(identifier))

        depth += 1
        for child in children:
            self.(child, depth)  # recursive call

    def traverse(self, identifier, mode=_DEPTH):
        # Python generator. Loosly based on an algorithm from 
        # 'Essential LISP' by John R. Anderson, Albert T. Corbett, 
        # and Brian J. Reiser, page 239-241
        yield identifier
        queue = self[identifier].children
        while queue:
            yield queue[0]
            expansion = self[queue[0]].children
            if mode == _DEPTH:
                queue = expansion + queue[1:]  # depth-first
            elif mode == _BREADTH:
                queue = queue[1:] + expansion  # width-first

    def __getitem__(self, key):
        return self.__nodes[key]

    def __setitem__(self, key, item):
        self.__nodes[key] = item

class Node:
    def __init__(self, identifier):
        self.__identifier = identifier
        self.__children = []

    @property
    def identifier(self):
        return self.__identifier

    @property
    def children(self):
        return self.__children

    def add_child(self, identifier):
        self.__children.append(identifier)


"""
