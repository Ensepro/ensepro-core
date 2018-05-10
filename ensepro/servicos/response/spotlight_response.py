"""
@project ensepro
@since 10/04/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
from ensepro.conversores import make_json_serializable


class SpotlightResponse:

    def __init__(self, response):
        self.response = response
        self.as_json = response.json()

    def __to_json__(self):
        return self.as_json

    def __str__(self):
        return str(self.__to_json__())

    def __repr__(self):
        return self.__str__()
