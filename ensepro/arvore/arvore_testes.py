"""
@project ensepro
@since 18/12/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from ensepro.arvore.arvore import Arvore
from ensepro.arvore.arvore import Node
from nltk.tree import Tree

arvore = Arvore()
arvore.adicionar_node("a", "aa")
arvore.adicionar_node("b", "bb", "a")
arvore.adicionar_node("c", "cc", "a")
arvore.adicionar_node("d", "dd", "c")
arvore.adicionar_node("f", "ff", "b")
arvore.adicionar_node("g", "gg", "a")
arvore.adicionar_node("h", "hh", "c")

print(arvore)
Tree.fromstring(str(arvore)).pretty_print()

