"""
@project ensepro
@since 17/04/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from ensepro.constantes import LoggerConstantes
from ensepro.elasticsearch.searches import simple_search
from ensepro.servicos import dbpedia_spotlight_service, knowledge_graph_search_service
from ensepro.servicos.request import SpotlightRequest, KnowledgeGraphSearchRequest

logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_CONSULTA)

PROP_FIELDS_SEARCHES = ["subject.concept", "object.concept"]
LISTA_CONFIANCAS = [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]


def busca_no_elasticsearch(substantivo_proprio):
    for field_search in PROP_FIELDS_SEARCHES:
        logger.debug("Testando full match no campo '%s'", field_search)
        result = simple_search(field_search, substantivo_proprio)

        if result["hits"]["total"] > 0:
            logger.info("Full match encontrado para substantivo '%s'", substantivo_proprio)
            return {
                "field": field_search,
                "total_hits": result["hits"]["total"]
            }


def encontrar_entidade_spotlight(frase_original, substantivo_proprio, lang="pt"):
    base_request = SpotlightRequest(frase_original)
    spotlight_requests = base_request.replicate_for_confidences(LISTA_CONFIANCAS)
    responses = dbpedia_spotlight_service.spotlight_list(spotlight_requests, lang=lang)

    for response in responses:
        response_json = response.as_json
        logger.debug("Response: %s", response_json["@confidence"])
        if "Resources" in response_json:
            entities_found = response_json["Resources"]
            entities_found.sort(key=lambda entity: entity["@similarityScore"], reverse=False)

            for entity in entities_found:
                uri = entity["@URI"]
                entity_name = uri[uri.rfind("/") + 1:]

                if (entity_name == substantivo_proprio):
                    return {"result": "Entidade encontrada pelo Spotlight é igual ao substantivo próprio"}

                if (substantivo_proprio.replace("_", " ").lower() in entity["@surfaceForm"].lower()):
                    es_result = busca_no_elasticsearch(entity_name)
                    if es_result:
                        return {
                            "nova_frase": frase_original.replace(entity["@surfaceForm"], entity_name[:1].upper() + entity_name[1:].lower()),
                            "result": es_result
                        }

    return None


def encontrar_entidade_google_knowledge_graph(frase_original, substantivo_proprio, lang="pt"):
    request = KnowledgeGraphSearchRequest(substantivo_proprio, languages=lang)
    result = knowledge_graph_search_service.search(request).as_json

    for item in result["itemListElement"]:
        if "name" in item["result"]:
            entity = item["result"]["name"]
            es_result = busca_no_elasticsearch(entity)
            if es_result:
                return {
                    "nova_frase": frase_original.replace(entity["@surfaceForm"], entity[:1].upper() + entity[1:].lower()),
                    "result": es_result
                }
        return None


class ReferenciasSubstantivosProprios:

    def __init__(self, frase):
        self.frase = frase
        self.__should_call_spotlight = True
        self.__resultado_referencias = {}

    @property
    def resultado_referencias(self):
        return [(substantivo_proprio, resultado) for substantivo_proprio, resultado in self.__resultado_referencias.items() if resultado]

    def localizar(self):
        substantivos_proprios = self.__list_substantivos_proprios()
        if not substantivos_proprios:
            return None
        for substantivo_proprio in substantivos_proprios:
            self.__resultado_referencias[substantivo_proprio] = self.__localizar_referencia(substantivo_proprio)

    def __localizar_referencia(self, substantivo_proprio):
        elasticsearch_result = busca_no_elasticsearch(substantivo_proprio.palavra_canonica)

        if elasticsearch_result:
            return {
                "match": "full",
                "find_key": substantivo_proprio,
                "field": elasticsearch_result["field"],
                "matches_found": elasticsearch_result["total_hits"]
            }

        spotlight_response = encontrar_entidade_spotlight(self.frase.frase_original, substantivo_proprio.palavra_canonica)
        if spotlight_response:
            return spotlight_response

        spotlight_response = encontrar_entidade_spotlight(self.frase.frase_original, substantivo_proprio.palavra_canonica, lang="en")
        if spotlight_response:
            return spotlight_response

        knowledge_graph = encontrar_entidade_google_knowledge_graph(self.frase.frase_original, substantivo_proprio.palavra_canonica)
        if knowledge_graph:
            return knowledge_graph

        knowledge_graph = encontrar_entidade_google_knowledge_graph(self.frase.frase_original, substantivo_proprio.palavra_canonica, lang="en")
        if knowledge_graph:
            return knowledge_graph

        return None

    def __list_substantivos_proprios(self):
        return self.frase.get_palavras(self.__is_substantivo_proprio)

    def __is_substantivo_proprio(self, frase, palavra, *args):
        return bool(palavra.is_substantivo_proprio())
