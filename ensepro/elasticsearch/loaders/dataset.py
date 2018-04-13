"""
@project ensepro
@since 04/03/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import re
import json
from ensepro.servicos.palavras_service import analisar_frase
from ensepro.constantes import LoggerConstantes, StringConstantes
from ensepro.elasticsearch import helpers, loaders

logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_ES_DATASET)


def carregar_dataset(es_client, index_name, index_type, index_settings,
                     dataset_file, delete_index_before=False):
    helpers.create_index(es_client, index_name, index_settings, delete_index_before=delete_index_before)

    linhas_dataset = open(dataset_file,
                          StringConstantes.FILE_READ_ONLY,
                          encoding=StringConstantes.UTF_8).read().split(StringConstantes.BREAK_LINE)

    acoes_insercao = __converter_para_insert_actions(index_name, index_type, linhas_dataset)

    print(json.dumps(acoes_insercao, indent=4, sort_keys=False))


def __converter_para_insert_actions(index_name, index_type, linhas_dataset):
    acoes = []
    for linha in linhas_dataset:
        source = __build_source(linha)
        if source:
            acao = loaders.criar_acao_insercao(index_name, index_type, source)
            acoes.append(acao)

    return acoes


def __build_source(linha):
    values = re.findall('[<"]([^<">]*)[">]', linha)
    if values:
        return __criar_tripla(values)
    return None


def __criar_tripla(triple):
    return {
        "sujeito": __criar_elemento(triple[0]),
        "predicado": __criar_elemento(triple[1]),
        "objeto": __criar_elemento(triple[2])
    }


def __criar_elemento(elemento):
    if __is_uri(elemento):
        split_at = elemento.rfind("/")
        conceito = elemento[split_at + 1:]
        uri = elemento[:split_at]
        return {
            "texto_original": elemento,
            "conceito": conceito,
            "uri": uri
        }

    return {"conceito": elemento}


def __is_uri(value):
    return value.startswith("http")
