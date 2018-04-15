"""
@project ensepro
@since 14/04/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
from ensepro.constantes import LoggerConstantes

query = {
    "query": {
        "query_string": {
            "fields": [],
            "query": ""
        }
    }
}

logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_ES_QUERIES)


class SimpleQuerySearch:

    def __init__(self):
        self.__fields = []
        self.__values = []
        self.__operation = None

    def operation(self, operation):
        self.__operation = operation

    def add_field(self, field):
        if field not in self.__fields:
            self.__fields.append(field)

    def add_value(self, value):
        if value not in self.__values:
            self.__values.append(value)

    def build_query(self):
        if self.__operation or len(self.__values) == 1:
            query["query"]["query_string"]["fields"] = self.__fields
            query["query"]["query_string"]["query"] = self.__operation.join(self.__values) if self.__operation else self.__values[0]
            logger.debug("SimpleQuerySearch criada: %s", query)
            return query

        exception = Exception("Operação deve ser definida quando 'values' possuí multiplos valores.")
        logger.exception(exception, exc_info=False)
        raise exception
