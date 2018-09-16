"""
@project ensepro
@since 10/04/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import requests
from ensepro.servicos.request import KnowledgeGraphSearchRequest
from ensepro.servicos.response import KnowledgeGraphSearchResponse
import ensepro.configuracoes as configuracoes
from ensepro.constantes import LoggerConstantes, KnowledgeGraphSearchConstantes

logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_KNOWLEDGE_GRAPH_SEARCH_SERVICE)
api_key = open(configuracoes.get_config(KnowledgeGraphSearchConstantes.API_KEY)).read()
endpoint = configuracoes.get_config(KnowledgeGraphSearchConstantes.ENDPOINT)
search_service = configuracoes.get_config(KnowledgeGraphSearchConstantes.SEARCH_SERVICE)


def search(request: KnowledgeGraphSearchRequest) -> KnowledgeGraphSearchResponse:
    logger.info("Service Knowledge Graph Search request: [request=%s]", request)

    url = __build_url([endpoint, search_service])
    params = request.__dict__

    logger.debug("Executando request [url=%s, params=%s]", url, params)

    # Setando API_KEY após o log para não salvar nos logs.
    params["key"] = api_key
    response = requests.get(url, params=params)

    logger.info("Service Knowledge Graph Search response: [response=%s]", response)

    if (response.ok):
        # logger.debug("Response as json: [response=%s]", response.json())
        return KnowledgeGraphSearchResponse(response)

    # Se respose não OK, lança exception
    exception = Exception("Erro ao chamar servico do Knowledge Graph Search: [status_code={0}, reason={1}, response_text={2}]" \
                          "".format(response.status_code, response.reason, response.text))

    logger.exception(exception, exc_info=False)
    raise exception


def __build_url(values):
    return ''.join(values)


if __name__ == '__main__':
    import sys

    if len(sys.argv) <= 1:
        print("é necessário passar um parametro. 'texto'")
        exit(1)

    print(search(KnowledgeGraphSearchRequest(sys.argv[1])))
