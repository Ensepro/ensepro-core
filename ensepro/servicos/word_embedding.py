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
simple_cache = {}


def word_embedding(palavra1, palavra2):
    if not palavra1 or not palavra2:
        return 0
    palavra1 = palavra1.lower()
    palavra2 = palavra2.lower()
    logger.debug("Verificando similaridade entra palavras: %s - %s", palavra1, palavra2)

    if string_key(palavra1, palavra2) in simple_cache:
        out = simple_cache.get(string_key(palavra1, palavra2))
        logger.debug("[CACHE] word_embedding em cache. [%s]", out)
        return out

    url = __build_url([endpoint, ":", porta, servico_word_embedding, "/"])
    data = {"word1": palavra1, "word2": palavra2}
    logger.debug("Executando request [url=%s, data=%s]", url, data)

    response = requests.post(url, json=data)
    # logger.info("similaridade: [response=%s]", response)

    if response.ok:
        logger.debug("Response as json: [response=%s]", response.json())
        out = response.json()["score"]
        simple_cache[string_key(palavra1, palavra2)] = out
        return out

    # Se respose não OK, throw exception
    exception = HTTPError("Erro ao chamar o serviço WordEmbedding: [status_code={0}, reason={1}]" \
                          "".format(response.status_code, response.reason), response=response)
    raise exception


def n_word_embedding(palavras1, palavras2):
    if not palavras1 or not palavras2:
        return 0
    palavras1 = [palavra.lower() for palavra in palavras1]
    palavras2 = [palavra.lower() for palavra in palavras2]
    logger.debug("Verificando similaridade entra palavras: %s - %s", palavras1, palavras2)

    if list_key(palavras2, palavras2) in simple_cache:
        out = simple_cache.get(list_key(palavras1, palavras2))
        logger.debug("[CACHE] n_word_embedding em cache. [%s]", out)
        return out

    url = __build_url([endpoint, ":", porta, '/word-embedding/n-similarity/'])
    data = {"words1": palavras1, "words2": palavras2}
    logger.debug("Executando request [url=%s, data=%s]", url, data)

    response = requests.post(url, json=data)
    if response.ok:
        logger.debug("Response as json: [response=%s]", response.json())
        out = response.json()["score"]
        simple_cache[list_key(palavras1, palavras2)] = out
        return out

    # Se respose não OK, throw exception
    exception = HTTPError(
        "Erro ao chamar o serviço WordEmbedding with ({palavras1} - {palavras2} [status_code={0}, reason={1}]".format(
            response.status_code,
            response.reason,
            palavras1=str(palavras1),
            palavras2=str(palavras2)
        ),
        response=response)

    logger.exception(exception)
    simple_cache[list_key(palavras1, palavras2)] = 0
    return 0


def string_key(palavra1, palavra2):
    return "{}+{}".format(palavra1, palavra2)


def list_key(palavras1: list, palavras2: list):
    palavras1.sort()
    palavras2.sort()

    key1 = '-'.join(palavras1)
    key2 = '-'.join(palavras2)

    return '+'.join([key1, key2])


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
