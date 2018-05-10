"""
@project ensepro
@since 07/05/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from ensepro import LoggerConstantes

query = {
    "query": {
        "term": {
        }
    }
}

logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_ES_QUERIES)


class SimpleQueryTermSearch:

    def __init__(self, field, value):
        self.__field = field
        self.__value = value

    def build_query(self):
        query["query"]["term"][self.__field] = self.__value
        logger.debug("SimpleQueryTermSearch criada: %s", query)
        return query
