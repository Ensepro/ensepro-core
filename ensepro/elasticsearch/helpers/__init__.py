"""
@project ensepro
@since 04/03/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from ensepro.constantes import LoggerConstantes

logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_ES_HELPERS)


def create_index(es_client, index_name, index_settings, delete_index_before=False):
    if delete_index_before:
        delete_index(es_client, index_name)
    logger.info("Criando índice {}".format(index_name))
    es_client.indices.create(index=index_name, body=index_settings)


def delete_index(es_client, index_name):
    logger.debug("Removendo índice '{}'".format(index_name))
    es_client.indices.delete(index=index_name, ignore=[400, 404])
