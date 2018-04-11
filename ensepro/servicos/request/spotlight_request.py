"""
@project ensepro
@since 10/04/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
from ensepro.conversores import make_json_serializable


class SpotlightRequest:
    def __init__(self, text, confidence=0, support=0):
        self.text = text
        self.confidence = confidence
        self.support = support

    def __to_json__(self):
        return self.__dict__

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()
