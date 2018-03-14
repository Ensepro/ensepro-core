"""
@project ensepro
@since 12/04/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""


class Query:

    def __init__(self, index_name, index_type, query, params=None):
        self.index_name = index_name
        self.index_type = index_type
        self.query = query
        self.params = params

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()
