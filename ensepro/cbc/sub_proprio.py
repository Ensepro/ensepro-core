# -*- coding: utf-8 -*-
"""
@project ensepro
@since 02/07/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from ensepro import LoggerConstantes, Frase, DBPediaSpotlightConstantes
from ensepro import configuracoes
from ensepro.cbc.fields import Field
from ensepro.elasticsearch.searches import full_match_serach
from ensepro.servicos import dbpedia_spotlight_service, knowledge_graph_search_service
from ensepro.servicos.request import SpotlightRequest, KnowledgeGraphSearchRequest

fields = [Field.FULL_MATCH_SUJEITO, Field.FULL_MATCH_PREDICADO, Field.FULL_MATCH_OBJETO]
confiancas = configuracoes.get_config(DBPediaSpotlightConstantes.CONFIANCAS)
logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_CBC)


def busca_no_elasticsearch(substantivo_proprio):
    search_result = full_match_serach(fields, substantivo_proprio)
    if search_result["keys"]:
        return search_result


def remove_small_words(substantivo_proprio):
    # TODO mover para utilizar `stop words` do nltk
    count = 0
    i = 0
    final = ""
    while i <= len(substantivo_proprio):
        if i == len(substantivo_proprio):
            if count > 2:
                final += substantivo_proprio[:count + 1]
            break
        w = substantivo_proprio[i]
        if (w == "_"):
            if count > 2:
                final += substantivo_proprio[:count + 1]

            substantivo_proprio = substantivo_proprio[count + 1:]
            i = 0
            count = 0
            continue

        count += 1
        i += 1

    return final


def encontrar_entidade_spotlight(frase_original, substantivo_proprio, lang):
    base_request = SpotlightRequest(frase_original)
    spotlight_requests = base_request.replicate_for_confidences(confiancas)
    responses = dbpedia_spotlight_service.spotlight_list(spotlight_requests, lang=lang)
    frase_temp = frase_original
    for response in responses:
        temp_substantivo_proprio = substantivo_proprio
        response_json = response.as_json
        logger.debug("Response with confidence: %s", response_json["@confidence"])
        if "Resources" in response_json:
            entities_found = response_json["Resources"]
            entities_found.sort(key=lambda entity: entity["@similarityScore"], reverse=False)

            for entity in entities_found:
                temp_substantivo_proprio = remove_small_words(temp_substantivo_proprio)
                if not temp_substantivo_proprio:
                    break

                uri = entity["@URI"]
                entity_name = uri[uri.rfind("/") + 1:]
                entity_name_lower = entity_name.lower()

                if entity_name_lower == temp_substantivo_proprio:
                    # es_result = busca_no_elasticsearch(entity_name)
                    logger.debug("Substantivo próprio encontrado no spotlight igual ao da frase.")
                    return {
                        "nova_frase": frase_original,
                        "reanalisar": False
                    }

                surface = remove_small_words(entity["@surfaceForm"].lower().replace(" ", "_"))

                if temp_substantivo_proprio in surface:
                    logger.debug("Substantivo próprio do spotlight contém o substantivo próprio da frase")
                    es_result = busca_no_elasticsearch(entity_name_lower)
                    if es_result:
                        temp_substantivo_proprio = temp_substantivo_proprio.replace(surface, "")
                        frase_temp = frase_temp.replace(entity["@surfaceForm"],
                                                                "<split> " + entity_name + " <split>")

                        if not temp_substantivo_proprio:
                            return {
                                "nova_frase": frase_temp
                            }
                    else:
                        logger.debug("Substantivo próprio ingorado. (Não existe no elasticsearch) ")

                elif temp_substantivo_proprio != substantivo_proprio and surface in temp_substantivo_proprio:
                    es_result = busca_no_elasticsearch(entity_name_lower.replace("_", " "))
                    if es_result:
                        temp_substantivo_proprio = temp_substantivo_proprio.replace(surface, "")
                        frase_temp = frase_temp.replace(entity["@surfaceForm"],
                                                                "<split> " + entity_name + " <split>")

                        if not temp_substantivo_proprio:
                            return {
                                "nova_frase": frase_temp
                            }
                    else:
                        logger.debug("Substantivo próprio ingorado. (Não existe no elasticsearch) ")

    return {
        "nova_frase": frase_original
    }


def encontrar_entidade_google_knowledge_graph(frase_original, substantivo_proprio, lang):
    request = KnowledgeGraphSearchRequest(substantivo_proprio, languages=lang)
    result = knowledge_graph_search_service.search(request).as_json

    for item in result["itemListElement"]:
        if "name" in item["result"]:
            entity = item["result"]["name"].lower()
            if substantivo_proprio.replace("_", " ") in entity.lower():
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
    # encontrar_entidade_spotlight_en,
    # encontrar_entidade_google_knowledge_graph_pt,
    # encontrar_entidade_google_knowledge_graph_en,
]


def remover_adjuntos_adnominais_justapostos(ensepro_result: Frase):
    logger.info("Removendo adjuntos adnominais justapostos")
    palavras = ensepro_result.palavras
    index = len(palavras) - 1

    nova_frase = []

    while index >= 0:
        atualPalavra = palavras[index]
        index -= 1

        if atualPalavra.palavra_original:
            nova_frase.append(atualPalavra)

        if not atualPalavra.is_substantivo_proprio():
            continue

        if "<np-close>" not in atualPalavra.tags:
            continue

        if index > 0 and not (palavras[index].is_adjetivo() or palavras[index].is_substantivo()):
            continue

        proximaPalavra = palavras[index]
        index -= 1  # já sei que posso remover/ignorar a proximaPalavra
        logger.info("Removendo adjunto nominal: %s", proximaPalavra)

        while index >= 0:
            if "<np-close>" not in proximaPalavra.tags:
                break
            proximaPalavra = palavras[index]
            index -= 1

    resultado = ""
    for palavra in nova_frase[::-1]:
        palavra_original = palavra.palavra_original
        if not palavra.is_substantivo_proprio():
            palavra_original = palavra_original.replace("_", " ")
        else:
            palavra_original = "<split> " + palavra_original + " <split>"

        resultado += " " + palavra_original

    logger.info("Frase após remoção adjunto adnominais justapostos: %s", resultado)
    return resultado


# def remove_substantivos_proprios_existentes_no_es(substantivos_proprios):
#     lista_atualizada = []
#     logger.info("verificando existencia dos substantivos proprios no elasticsearch")
#     for substantivo_proprio in substantivos_proprios:
#         es_result = busca_no_elasticsearch(substantivo_proprio.palavra_canonica.lower().replace("_", " "))
#         if not es_result:
#             logger.info("mantendo substantivo [%s] pois não existe no elasticsearch", substantivo_proprio)
#             lista_atualizada.append(substantivo_proprio)
#         else:
#             logger.info("ignorando substantivo [%s] pois existe no elasticsearch", substantivo_proprio)
#
#     return lista_atualizada


def atualizar_frase(frase: Frase):
    logger.info("Atualizando frase.")
    substantivos_proprios = __list_substantivos_proprios(frase)
    if not substantivos_proprios:
        return frase

    # substantivos_proprios = remove_substantivos_proprios_existentes_no_es(substantivos_proprios)

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

    import ensepro
    if atualizou:
        frase = ensepro.analisar_frase(frase_original)

    if not has_adjunto_nominal_justaposto(frase):
        logger.info("Frase não possui adjuntos nominais justaposos.")
        return frase

    frase_sem_aa_justaposto = remover_adjuntos_adnominais_justapostos(frase)
    return ensepro.analisar_frase(frase_sem_aa_justaposto)


def has_adjunto_nominal_justaposto(frase: Frase):
    palavras = frase.get_palavras(__condicao_palavra_original_nao_vazia)

    for palavra in palavras:
        if palavra.is_substantivo_proprio() and "<np-close>" in palavra.tags:
            return True

    return False


def __list_substantivos_proprios(frase):
    return frase.get_palavras(__is_substantivo_proprio)


def __is_substantivo_proprio(frase, palavra, *args):
    return bool(palavra.is_substantivo_proprio())


def __condicao_palavra_original_nao_vazia(frase, palavra, *args) -> bool:
    if palavra.palavra_original and palavra.palavra_original.strip():
        return True
    return False
