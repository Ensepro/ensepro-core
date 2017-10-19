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
from utils.JsonUtil import save_to_json
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
    info("Frase{id} - ElasticSearch - Iniciando consulta ao ElasticSearch".format(id=frase_id))

    qb = QueryBuilder()
    qb.add_field("subject.concept").add_field("predicate.concept").add_field("object.concept")

    for palavra_relevante in frase_processada[PALAVRAS_RELEVANTES]:
        qb.add_value(palavra_relevante.palavraCanonica)

        debug("Frase{id} - ElasticSearch - buscando sinonimos da palavra '{palavra}'".format(id=frase_id, palavra=palavra_relevante.palavraCanonica))
        sinonimos = palavra_relevante.getSinonimos()
        for lang in sinonimos:
            for sinonimo in sinonimos[lang]:
                qb.add_value(sinonimo.sinonimo)

    debug("Frase{id} - QueryBuilder - dados: {qb}".format(id=frase_id, qb=str(qb)))

    query = qb.buildQuery()
    info("Frase{id} - ElasticSearch - Query construída.".format(id=frase_id))

    info("Frase{id} - ElasticSearch - Executando query.".format(id=frase_id))
    debug("Frase{id} - query={query}".format(id=id, query=query))

    results = ES.search(index=ES_SETTINGS[INDEX_NAME], doc_type=ES_SETTINGS[INDEX_TYPE], body=query)

    info("Frase{id} - ElasticSearchUtil - query executada... salvando resultado em arquivo json.".format(id=frase_id))

    save_to_json("frase{}_resultados_completo.json".format(frase_id), results)
    save_to_json("frase{}_resultados_resumidos.json".format(frase_id), __resumirResultados(results))




def __resumirResultados(resultado):
    resultado = resultado["hits"]["hits"]

    resultadoResumido = []

    for result in resultado:
        resultadoResumido.append(result["_source"])

    return resultadoResumido

