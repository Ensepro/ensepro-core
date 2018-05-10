# -*- coding: utf-8 -*-
"""
@project ensepro
@since 25/02/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
from ensepro.conversores import make_json_serializable
from ensepro.classes.palavra import ClasseGramatical


class Sinonimo:

    def __init__(self, **kwargs):
        self.synset = kwargs['synset'] if kwargs else None
        self.sinonimo = kwargs['sinonimo'] if kwargs else ''
        self.classe_gramatical = ClasseGramatical(kwargs['classe_gramatical']) if kwargs else None
        self.distancia_semantica = kwargs['distancia_semantica'] if kwargs else None

    def is_mesma_classe_gramatical(self, palavra):
        return self.classe_gramatical == palavra.classe_gramatical

    def __to_json__(self):
        return self.__dict__

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return self.sinonimo == other.sinonimo

    def __str__(self):
        return self.sinonimo

    def __repr__(self):
        return self.__str__()

    def as_text(self) -> str:
        return '.'.join([self.synset, self.classe_gramatical.value, self.distancia_semantica, self.sinonimo])

    @classmethod
    def from_list_string(cls, wordnet_sinonimos: list):
        return [cls.from_string(wordnet_sinonimo) for wordnet_sinonimo in wordnet_sinonimos]

    @classmethod
    def from_string(cls, wordnet_sinonimo: str):
        partes = wordnet_sinonimo.split(".")

        return cls(
                synset=partes[0],
                classe_gramatical=partes[1],
                distancia_semantica=partes[2],
                sinonimo=partes[3]
        )
