"""
@project ensepro
@since 07/05/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from ensepro import LoggerConstantes

logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_ES_QUERIES)


class QueryTermsSearch:

    def __init__(self, field, values=list()):
        self.__field = field
        self.__values = values

    def __query(self):
        return {
            "size": 10000,
            "query": {
                "terms": {
                }
            }
        }

    def add_value(self, value):
        self.__values.append(value)

    def build_query(self):
        query = self.__query()
        query["query"]["terms"][self.__field] = self.__values
        logger.debug("QueryTermsSearch criada: %s", query)
        return query
