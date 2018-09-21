# -*- coding: utf-8 -*-
"""
@project ensepro
@since 02/07/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from ensepro import LoggerConstantes, Frase, DBPediaSpotlightConstantes
from ensepro.cbc.fields import Field
from ensepro.elasticsearch.searches import full_match_serach
from ensepro.servicos import dbpedia_spotlight_service, knowledge_graph_search_service
from ensepro.servicos.request import SpotlightRequest, KnowledgeGraphSearchRequest
from ensepro import configuracoes

fields = [Field.FULL_MATCH_SUJEITO, Field.FULL_MATCH_PREDICADO, Field.FULL_MATCH_OBJETO]
confiancas = configuracoes.get_config(DBPediaSpotlightConstantes.CONFIANCAS)
logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_CBC)


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
                entity_name = uri[uri.rfind("/") + 1:]
                entity_name_lower = entity_name.lower()

                if (entity_name_lower == substantivo_proprio):
                    # es_result = busca_no_elasticsearch(entity_name)
                    logger.debug("Substantivo próprio encontrado no spotlight igual ao da frase.")
                    return {
                        "nova_frase": frase_original,
                        "reanalisar": False
                    }

                if (substantivo_proprio.replace("_", " ") in entity["@surfaceForm"].lower()):
                    logger.debug("Substantivo próprio do spotlight contém o substantivo próprio da frase")
                    es_result = busca_no_elasticsearch(entity_name_lower)
                    if es_result:
                        return {
                            "nova_frase": frase_original.replace(entity["@surfaceForm"], entity_name),
                            "resultado": es_result
                        }
                    logger.debug("Substantivo próprio ingorado. (Não existe no elasticsearch) ")


def encontrar_entidade_google_knowledge_graph(frase_original, substantivo_proprio, lang):
    request = KnowledgeGraphSearchRequest(substantivo_proprio, languages=lang)
    result = knowledge_graph_search_service.search(request).as_json

    for item in result["itemListElement"]:
        if "name" in item["result"]:
            entity = item["result"]["name"].lower()
            if (substantivo_proprio.replace("_", " ") in entity.lower()):
                logger.debug("Substantivo próprio do GKG contém o substantivo próprio da frase")
                es_result = busca_no_elasticsearch(entity)
                if es_result:
                    init = frase_original.lower().index(substantivo_proprio.replace("_", " "))
                    end = init + len(substantivo_proprio)
                    surfaseFrom = frase_original[init:end]
                    novo_termo = (entity[:1].upper() + entity[1:].lower()).replace(" ", "_")
                    return {
                        "nova_frase": frase_original.replace(surfaseFrom, novo_termo),
                    }
                logger.debug("Substantivo próprio ingorado. (Não existe no elasticsearch) ")

        return None


def encontrar_entidade_google_knowledge_graph_pt(frase_original, substantivo_proprio):
    logger.debug("Buscando substantivo próprio no GKG-PT")
    return encontrar_entidade_google_knowledge_graph(frase_original, substantivo_proprio, "pt")


def encontrar_entidade_google_knowledge_graph_en(frase_original, substantivo_proprio):
    logger.debug("Buscando substantivo próprio no GKG-EN")
    return encontrar_entidade_google_knowledge_graph(frase_original, substantivo_proprio, "en")


def encontrar_entidade_spotlight_pt(frase_original, substantivo_proprio):
    logger.debug("Buscando substantivo próprio no Spotlight-PT")
    return encontrar_entidade_spotlight(frase_original, substantivo_proprio, "pt")


def encontrar_entidade_spotlight_en(frase_original, substantivo_proprio):
    logger.debug("Buscando substantivo próprio no Spotlight-EN")
    return encontrar_entidade_spotlight(frase_original, substantivo_proprio, "en")


actions = [
    encontrar_entidade_spotlight_pt,
    encontrar_entidade_spotlight_en,
    encontrar_entidade_google_knowledge_graph_pt,
    encontrar_entidade_google_knowledge_graph_en,
]


def remover_cn_justaposto(ensepro_result: Frase):
    palavras = ensepro_result.palavras
    size = len(palavras)
    i = 0

    frase_sem_cn_justaposto = []

    while i < size - 1:
        palavra = palavras[i]
        nextPalavra = palavras[i + 1]
        i += 1

        canConsiderToIgnore = palavra.is_adjetivo() or palavra.is_substantivo()
        if "<np-close>" in nextPalavra.tags and canConsiderToIgnore:
            continue

        if palavra.palavra_original:
            frase_sem_cn_justaposto.append(palavra.palavra_original)

    if palavras[-1].palavra_original:
        frase_sem_cn_justaposto.append(palavras[-1].palavra_original)

    return ' '.join(frase_sem_cn_justaposto)


def atualizar_frase(frase: Frase):
    logger.info("Atualizando frase.")
    substantivos_proprios = __list_substantivos_proprios(frase)
    if not substantivos_proprios:
        return frase

    frase_original = frase.frase_original
    atualizou = False
    for substantivo_proprio in substantivos_proprios:
        for action in actions:
            logger.debug("Atualizando substantivo próprio (%s)com action: %s", substantivo_proprio, action.__name__)
            result = action(frase_original, substantivo_proprio.palavra_canonica.lower())
            logger.debug("Resultado da action (%s): %s", action.__name__, result)
            if result:
                result = result.get("nova_frase", None)
                if result:
                    atualizou = True
                    frase_original = result
                    break

    if atualizou:
        import ensepro
        substantivo_proprio_result = ensepro.analisar_frase(frase_original)
        frase_sem_cn_justaposto = remover_cn_justaposto(substantivo_proprio_result)
        return ensepro.analisar_frase(frase_sem_cn_justaposto)

    return frase


def __list_substantivos_proprios(frase):
    return frase.get_palavras(__is_substantivo_proprio)


def __is_substantivo_proprio(frase, palavra, *args):
    return bool(palavra.is_substantivo_proprio())


def __condicao_palavra_original_nao_vazia(frase, palavra, *args) -> bool:
    if palavra.palavra_original and palavra.palavra_original.strip():
        return True
    return False
