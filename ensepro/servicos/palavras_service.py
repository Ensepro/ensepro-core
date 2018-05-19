# -*- coding: utf-8 -*-
"""
@project ensepro
@since 25/02/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import requests
from requests import HTTPError

import ensepro.configuracoes as configuracoes
from ensepro.constantes import PalavrasServidorConstantes as ps_consts, LoggerConstantes as logger_consts

logger = logger_consts.get_logger(logger_consts.MODULO_PALAVRAS_SERVICE)

endpoint = configuracoes.get_config(ps_consts.ENDPOINT)
porta = configuracoes.get_config(ps_consts.PORTA)
servico_analisar_frase = configuracoes.get_config(ps_consts.SERVICO_ANALISAR_FRASE)


# TODO verificar a necessidade de uma classe de Request e Response
# TODO 2. futuro: implementar no PalavrasService um serviço que recebe uma lista de frase
#           e faz a analise delas e retorna tudo de uma vez... (acho que fica melhor do que ficar chamando toda hora...)
def analisar_frase(frase: str):
    logger.info("Analisando frase: [frase=%s]", frase)

    url = __build_url([endpoint, ":", porta, servico_analisar_frase])
    params = {"frase": frase}
    logger.debug("Executando request [url=%s, params=%s]", url, params)

    response = requests.get(url, params=params)
    logger.info("Frase analisada: [response=%s]", response)

    if (response.ok):
        logger.debug("Response as json: [response=%s]", response.json())
        return response

    # Se respose não OK, throw exception
    exception = HTTPError("Erro ao chamar o serviço PalavrasService: [status_code={0}, reason={1}]" \
                          "".format(response.status_code, response.reason), response=response)
    raise exception


def __build_url(values):
    return ''.join(values)
