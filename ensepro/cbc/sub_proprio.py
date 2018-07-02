# -*- coding: utf-8 -*-
"""
@project ensepro
@since 02/07/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from ensepro import LoggerConstantes, Frase
from ensepro.consulta.fields import Field
from ensepro.elasticsearch.searches import full_match_serach
from ensepro.servicos import dbpedia_spotlight_service, knowledge_graph_search_service
from ensepro.servicos.request import SpotlightRequest, KnowledgeGraphSearchRequest

fields = [Field.FULL_MATCH_SUJEITO, Field.FULL_MATCH_PREDICADO, Field.FULL_MATCH_OBJETO]
confiancas = [0.8, 0.5]
logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_CONSULTA)


def busca_no_elasticsearch(substantivo_proprio):
    search_result = full_match_serach(fields, substantivo_proprio)
    if search_result["keys"]:
        return search_result


def encontrar_entidade_spotlight(frase_original, substantivo_proprio, lang):
    base_request = SpotlightRequest(frase_original)
    spotlight_requests = base_request.replicate_for_confidences(confiancas)
    responses = dbpedia_spotlight_service.spotlight_list(spotlight_requests, lang=lang)

    for response in responses:
        response_json = response.as_json
        logger.debug("Response with confidence: %s", response_json["@confidence"])
        if "Resources" in response_json:
            entities_found = response_json["Resources"]
            entities_found.sort(key=lambda entity: entity["@similarityScore"], reverse=False)

            for entity in entities_found:
                uri = entity["@URI"]
                entity_name = uri[uri.rfind("/") + 1:].lower()

                if (entity_name == substantivo_proprio):
                    es_result = busca_no_elasticsearch(entity_name)
                    return {
                        "nova_frase": frase_original
                    }

                if (substantivo_proprio.replace("_", " ") in entity["@surfaceForm"].lower()):
                    es_result = busca_no_elasticsearch(entity_name)
                    if es_result:
                        return {
                            "nova_frase": frase_original.replace(entity["@surfaceForm"], entity_name[:1].upper() + entity_name[1:].lower()),
                            "resultado": es_result
                        }


def encontrar_entidade_google_knowledge_graph(frase_original, substantivo_proprio, lang):
    request = KnowledgeGraphSearchRequest(substantivo_proprio, languages=lang)
    result = knowledge_graph_search_service.search(request).as_json

    for item in result["itemListElement"]:
        if "name" in item["result"]:
            entity = item["result"]["name"].lower()
            if (substantivo_proprio.replace("_", " ") in entity.lower()):
                es_result = busca_no_elasticsearch(entity)
                if es_result:
                    init = frase_original.lower().index(substantivo_proprio)
                    end = init + len(substantivo_proprio)
                    surfaseFrom = frase_original[init:end]
                    novo_termo = (entity[:1].upper() + entity[1:].lower()).replace(" ", "_")
                    return{
                        "nova_frase": frase_original.replace(surfaseFrom, novo_termo),
                    }

        return None


def encontrar_entidade_google_knowledge_graph_pt(frase_original, substantivo_proprio):
    return encontrar_entidade_google_knowledge_graph(frase_original, substantivo_proprio, "pt")


def encontrar_entidade_google_knowledge_graph_en(frase_original, substantivo_proprio):
    return encontrar_entidade_google_knowledge_graph(frase_original, substantivo_proprio, "en")


def encontrar_entidade_spotlight_pt(frase_original, substantivo_proprio):
    return encontrar_entidade_spotlight(frase_original, substantivo_proprio, "pt")


def encontrar_entidade_spotlight_en(frase_original, substantivo_proprio):
    return encontrar_entidade_spotlight(frase_original, substantivo_proprio, "en")


actions = [
    encontrar_entidade_spotlight_pt,
    encontrar_entidade_spotlight_en,
    encontrar_entidade_google_knowledge_graph_pt,
    encontrar_entidade_google_knowledge_graph_en,
]


def atualizar_frase(frase: Frase):
    substantivos_proprios = __list_substantivos_proprios(frase)
    if not substantivos_proprios:
        return frase

    substantivo_proprio_result = None
    for substantivo_proprio in substantivos_proprios:
        for action in actions:
            result = action(frase.frase_original, substantivo_proprio.palavra_canonica.lower())
            if result:
                result = result.get("nova_frase", None)
                if result:
                    import ensepro
                    substantivo_proprio_result = ensepro.analisar_frase(result)
                    break

    if substantivo_proprio_result:
        return substantivo_proprio_result

    return frase



def __list_substantivos_proprios(frase):
    return frase.get_palavras(__is_substantivo_proprio)


def __is_substantivo_proprio(frase, palavra, *args):
    return bool(palavra.is_substantivo_proprio())
