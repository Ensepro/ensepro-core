"""
@project ensepro
@since 21/08/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from conversores import MakeJsonSerializable


class Sinonimo(object):
    def __init__(self, *args, **kwargs):
        sinonimo = args[0]
        self.numero = sinonimo["numero"]
        self.classeGramatical = sinonimo["classeGramatical"]
        self.distanciaSemantica = sinonimo["distanciaSemantica"]
        self.sinonimo = sinonimo["sinonimo"]

    def to_json(self):
        return self.__dict__

    def __str__(self):
        return self.sinonimo

    def __eq__(self, other):
        return self.sinonimo == other.sinonimo

    def __hash__(self):
        return self.numero
