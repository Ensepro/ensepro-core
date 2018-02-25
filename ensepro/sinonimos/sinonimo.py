"""
@project ensepro
@since 04/01/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
from ensepro.conversores import make_json_serializable
from ensepro.classes.palavra import ClasseGramatical


class Sinonimo:

    def __init__(self, **kwargs):
        self.synset = kwargs['synset'] if kwargs else None
        self.sinonimo = kwargs['sinonimo'] if kwargs else ''
        self.classe_gramatical = kwargs['classe_gramatical'] if kwargs else None
        self.distancia_semantica = kwargs['distancia_semantica'] if kwargs else None

    def is_mesma_classe_gramatical(self, palavra):
        if palavra.is_verbo():
            return self.classe_gramatical == ClasseGramatical.VERBO

        if palavra.is_adjetivo():
            return self.classe_gramatical == ClasseGramatical.ADJETIVO

        if palavra.is_substantivo():
            return self.classe_gramatical == ClasseGramatical.SUBSTANTIVO

        return False

    def to_json(self):
        return self.__dict__

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return str(self) == str(other)

    def __str__(self):
        return self.sinonimo

    def __repr__(self):
        return self.__str__()

    def as_text(self) -> str:
        return '.'.join([self.synset, self.classe_gramatical, self.distancia_semantica, self.sinonimo])

    @classmethod
    def from_string(cls, wordnet_sinonimo: str):
        partes = wordnet_sinonimo.split(".")

        return cls(
                synset=partes[0],
                classe_gramatical=partes[1],
                distancia_semantica=partes[2],
                sinonimo=partes[3]
        )
