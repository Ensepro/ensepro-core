"""
@project ensepro
@since 07/05/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from ensepro import LoggerConstantes

logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_ES_QUERIES)


class QueryTermSearch:

    def __init__(self, field, value):
        self.__field = field
        self.__value = value

    def __query(self):
        return {
            "size": 10000,
            "query": {
                "term": {
                }
            }
        }

    def build_query(self):
        query = self.__query()
        query["query"]["term"][self.__field] = self.__value
        logger.debug("QueryTermSearch criada: %s", query)
        return query
