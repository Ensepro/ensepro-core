"""
@project ensepro
@since 07/05/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from ensepro import LoggerConstantes

logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_ES_QUERIES)


class QueryMultiTermSearch:

    def __init__(self):
        self.__fields = []
        self.__values = []

    def __query(self):
        return {
            "size": 10000,
            "query": {
                "bool": {
                    "must": [

                    ]
                }
            }
        }

    def add_term_search(self, field, value):
        self.__fields.append(field)
        self.__values.append(value)

    def build_query(self):
        query = self.__query()

        for field, value in zip(self.__fields, self.__values):
            term = {
                "term": {
                    field.value["name"]: value
                }
            }
            query["query"]["bool"]["must"].append(term)

        logger.debug("QueryMultiTermSearch criada: %s", query)
        return query
