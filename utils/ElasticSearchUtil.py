"""
@project ensepro
@since 18/10/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import json
import configuracoes
from elasticsearch import Elasticsearch
from es.QueryBuilder import QueryBuilder
from utils.LogUtil import error, debug, info
from constantes.ElasticSerachConstantes import *
from constantes.NLUConstantes import PALAVRAS_RELEVANTES
from constantes.ConfiguracoesConstantes import CONFIG_ENDPOINT, CONFIG_PORTA, CONFIG_SETTINGS, SERVIDOR_ELASTIC_SEARCH, SAVE_FILES_TO

def initElasticSearch():
    es_host = configuracoes.getValue(CONFIG_ENDPOINT.format(nome_servidor=SERVIDOR_ELASTIC_SEARCH))
    es_port = configuracoes.getValue(CONFIG_PORTA.format(nome_servidor=SERVIDOR_ELASTIC_SEARCH))
    # TODO adicionar questão de usuário e senha
    global ES
    global ES_SETTINGS
    ES_SETTINGS = configuracoes.getElasticSearchSettings()
    ES = Elasticsearch([{'host': es_host, 'port': es_port}])


initElasticSearch()

def consultar(frase_processada, frase_id):
    qb = QueryBuilder()
    qb.add_field("subject.concept")

    for palavra_relevante in frase_processada[PALAVRAS_RELEVANTES]:
        qb.add_value(palavra_relevante.palavraCanonica)

        info("ElasticSearchUil - buscando sinonimos da palavra '{}'".format(palavra_relevante.palavraCanonica))
        sinonimos = palavra_relevante.getSinonimos()
        info("ElasticSearchUil - busca finalizada.")
        for lang in sinonimos:
            for sinonimo in sinonimos[lang]:
                qb.add_value(sinonimo.sinonimo)

    debug("QueryBuilder - dados: {}".format(str(qb)))

    query = qb.buildQuery()
    debug("ElasticSearchUtil - executando query: {}".format(query))

    results = ES.search(index=ES_SETTINGS[INDEX_NAME], doc_type=ES_SETTINGS[INDEX_TYPE], body=query)

    info("ElasticSearchUtil - query executada, salvando resultado em arquivo json.")

    with open(SAVE_FILES_TO.format(fileName="frase{}_es_result.json".format(frase_id)), "w+", encoding="utf-8") as result_file:
        result_file.write(json.dumps(results, ensure_ascii=False, indent=4, sort_keys=False))