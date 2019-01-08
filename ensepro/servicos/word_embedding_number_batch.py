import requests
import ensepro.configuracoes as configuracoes
from ensepro.constantes import LoggerConstantes, WordEmbeddingNumberBatchConstantes

logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_WORD_EMBEDDING_NUMBER_BATCH)
endpoint = configuracoes.get_config(WordEmbeddingNumberBatchConstantes.ENDPOINT)
service = configuracoes.get_config(WordEmbeddingNumberBatchConstantes.SERVICE)


def word_embedding(palavra1, palavra2):
    url = __build_url([endpoint, service]).format(palavra1=palavra1, palavra2=palavra2)
    logger.debug("Executando request [url=%s]", url)

    response = requests.get(url)
    logger.info("Service word embedding response: [response=%s]", response)

    if (response.ok):
        logger.debug("Response as json: [response=%s]", response.json())
        return response.json()

    # Se respose não OK, lança exception
    exception = Exception("Erro ao chamar servico do word_embedding: [status_code={0}, reason={1}, response_text={2}]" \
                          "".format(response.status_code, response.reason, response.text))

    logger.exception(exception, exc_info=False)
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
