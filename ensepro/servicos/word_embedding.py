# -*- coding: utf-8 -*-
"""
@project ensepro
@since 08/03/2019
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import requests
from requests import HTTPError

import ensepro.configuracoes as configuracoes
from ensepro.constantes import LoggerConstantes, WordEmbeddingServidorConstantes as wb_consts

logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_WORD_EMBEDDING)

endpoint = configuracoes.get_config(wb_consts.ENDPOINT)
porta = configuracoes.get_config(wb_consts.PORTA)
servico_word_embedding = configuracoes.get_config(wb_consts.SERVICO_WORD_EMBEDDING)


def word_embedding(palavra1, palavra2):
    logger.debug("Verificando similaridade entra palavras: %s - %s", palavra1, palavra2)

    url = __build_url([endpoint, ":", porta, servico_word_embedding])
    params = {"word1": palavra1, "word2": palavra2}
    logger.debug("Executando request [url=%s, params=%s]", url, params)

    response = requests.get(url, params=params)
    logger.info("similaridade: [response=%s]", response)

    if (response.ok):
        logger.debug("Response as json: [response=%s]", response.json())
        return response.json()["score"]

    # Se respose não OK, throw exception
    exception = HTTPError("Erro ao chamar o serviço WordEmbedding: [status_code={0}, reason={1}]" \
                          "".format(response.status_code, response.reason), response=response)
    raise exception


def __build_url(values):
    return ''.join(values)

if __name__ == '__main__':
    import sys

    if len(sys.argv) <= 2:
        print("São necessários pelo menos dois parametros. 'palavra1' e 'palavra2'")
        exit(1)

    palavra1 = sys.argv[1]
    palavra2 = sys.argv[2]

    print(word_embedding(palavra1, palavra2))
