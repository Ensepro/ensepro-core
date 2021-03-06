"""
@project ensepro
@since 12/04/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""


class Query:

    def __init__(self, index_name, index_type, query):
        self.index_name = index_name
        self.index_type = index_type
        self.query = query

    @classmethod
    def build_default(cls, query, _params=None):
        from ensepro import configuracoes
        from ensepro.constantes import ElasticSearchConstantes

        index_name = configuracoes.get_config(ElasticSearchConstantes.INDEX_NAME)
        index_type = configuracoes.get_config(ElasticSearchConstantes.INDEX_TYPE)

        return cls(
                index_name,
                index_type,
                query
        )

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()
