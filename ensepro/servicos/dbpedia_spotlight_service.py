"""
@project ensepro
@since 09/04/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import requests
from ensepro.servicos.request import SpotlightRequest
from ensepro.servicos.response import SpotlightResponse
import ensepro.configuracoes as configuracoes
from ensepro.constantes import LoggerConstantes, DBPediaSpotlightConstantes

logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_DBPEDIA_SPOTLIGHT_SERVICE)
endpoint = configuracoes.get_config(DBPediaSpotlightConstantes.ENDPOINT)
servico_spotlight = configuracoes.get_config(DBPediaSpotlightConstantes.SERVICO_SPOTLIGHT)


def spotlight(request: SpotlightRequest, lang="pt") -> SpotlightResponse:
    logger.info("Service Spotlight request: [request=%s]", request)

    url = __build_url([endpoint, servico_spotlight.format(lang=lang)])
    params = request.__dict__
    headers = {"Accept": "application/json"}
    logger.debug("Executando request [url=%s, params=%s, headers=%s]", url, params, headers)

    response = requests.get(url, params=params, headers=headers)
    logger.info("Service Spotlight response: [response=%s]", response)

    if (response.ok):
        logger.debug("Response as json: [response=%s]", response.json())
        return SpotlightResponse(response)

    # Se respose não OK, lança exception
    exception = Exception("Erro ao chamar servico do spotlight: [status_code={0}, reason={1}, response_text={2}]" \
                          "".format(response.status_code, response.reason, response.text))

    logger.exception(exception, exc_info=False)
    raise exception


def spotlight_list(requests, lang="pt"):
    return [spotlight(request, lang=lang) for request in requests]


def __build_url(values):
    return ''.join(values)


if __name__ == '__main__':
    import sys

    if len(sys.argv) <= 2:
        print("São necessários pelo menos dois parametros. 'texto' e 'confianca'")
        exit(1)

    text = sys.argv[1]
    confidence = sys.argv[2]
    support = 0
    if len(sys.argv) > 3:
        support = sys.argv[3]

    print(spotlight(SpotlightRequest(text, confidence, support)))
