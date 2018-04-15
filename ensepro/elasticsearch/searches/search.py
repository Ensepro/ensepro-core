"""
@project ensepro
@since 12/04/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
from ensepro.elasticsearch.queries import Query
from elasticsearch import Elasticsearch
from ensepro.constantes import LoggerConstantes

logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_ES_CONSULTA)


def execute_search(client: Elasticsearch, query: Query):
    logger.debug("Executando consulta simples: %s", query)
    return client.search(
            index=query.index_name,
            doc_type=query.index_type,
            body=query.query
    )
