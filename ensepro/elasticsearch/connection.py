"""
@project ensepro
@since 04/03/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
from ensepro import configuracoes
from elasticsearch import Elasticsearch
from ensepro.constantes import ElasticSearchConstantes, LoggerConstantes

logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_ES_CONNECTION)
__connection = None

def connection():
    global __connection
    if __connection:
        return __connection

    es_host = configuracoes.get_config(ElasticSearchConstantes.ENDPOINT)
    es_porta = configuracoes.get_config(ElasticSearchConstantes.PORTA)
    es_username = configuracoes.get_config(ElasticSearchConstantes.USERNAME)
    es_password = configuracoes.get_config(ElasticSearchConstantes.PASSWORD)

    endpoint = [{"host": es_host, "port": es_porta}]
    es_auth = None

    if es_username:
        es_auth = (es_username, es_password)

    logger.debug("Iniciando conexão com ElasticSeach[{}:{}]".format(es_host, es_porta))
    __connection = Elasticsearch(endpoint, http_auth=es_auth)
    return __connection
