"""
@project ensepro
@since 04/01/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from ensepro.conversores import make_json_serializable


class Sinonimo:

    def __init__(self, **kwargs):
        self.sinonimo = ''
        self.classe_gramatical = None
        self.distancia_semantica = None

        if kwargs:
            self.sinonimo = kwargs['sinonimo']
            self.classe_gramatical = kwargs['classe_gramatical']
            self.distancia_semantica = kwargs['distancia_semantica']

    def to_json(self):
        return self.__dict__

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return str(self) == str(other)

    def __str__(self):
        return '.'.join([self.classe_gramatical, self.distancia_semantica, self.sinonimo])

    @classmethod
    def from_string(cls, wordnet_sinonimo: str):
        partes = wordnet_sinonimo.split(".")
        kwargs = {}
        kwargs['classe_gramatical'] = partes[1]
        kwargs['distancia_semantica'] = partes[2]
        kwargs['sinonimo'] = partes[3]

        return cls(
                sinonimo=partes[3],
                classe_gramatical=partes[1],
                distancia_semantica=partes[2]
        )
