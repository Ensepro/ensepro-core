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

    # TODO review
    def __eq__(self, other):
        # if self.numero != other.numero:
        #    return False
        if self.classeGramatical != other.classeGramatical:
            return False
        if self.distanciaSemantica != other.distanciaSemantica:
            return False
        return self.sinonimo == other.sinonimo

    def __hash__(self):
        return self.numero
