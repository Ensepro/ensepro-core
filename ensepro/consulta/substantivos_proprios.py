"""
@project ensepro
@since 07/05/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
from ensepro import LoggerConstantes
from ensepro.consulta.fields import Field
from ensepro.elasticsearch.searches import full_match_serach
from ensepro.servicos import dbpedia_spotlight_service, knowledge_graph_search_service
from ensepro.servicos.request import SpotlightRequest, KnowledgeGraphSearchRequest

fields = [Field.FULL_MATCH_SUJEITO, Field.FULL_MATCH_PREDICADO, Field.FULL_MATCH_OBJETO]
confiancas = [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_CONSULTA)


# TODO Validar se a utilização do parcial_match aqui é melhor ou não(conversar com Denis) (fazer experimentos para validar)
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
                        "resultado": es_result
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
            es_result = busca_no_elasticsearch(entity)
            if es_result:
                return {
                    "nova_frase": frase_original.replace(entity["@surfaceForm"], entity[:1].upper() + entity[1:].lower()),
                    "resultado": es_result
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
    encontrar_entidade_google_knowledge_graph_en
    # TODO adicionar a busca simples ao ES com o substantivo_proprio. Se spotlight retornou entidade == :prop, vai buscar no ES, se não encontrar ali,
    # não vai encontrrar neste método também
]


class ReferenciasSubstantivosProprios:

    def __init__(self, frase):
        self.frase = frase
        self.__should_call_spotlight = True

    def localizar(self):
        substantivos_proprios = self.__list_substantivos_proprios()
        if not substantivos_proprios:
            return None

        substantivo_proprio_result = {}
        for substantivo_proprio in substantivos_proprios:
            for action in actions:
                result = action(self.frase.frase_original, substantivo_proprio.palavra_canonica.lower())
                if result:
                    substantivo_proprio_result[substantivo_proprio.palavra_canonica] = result
                    break

        return substantivo_proprio_result

    def __list_substantivos_proprios(self):
        return self.frase.get_palavras(self.__is_substantivo_proprio)

    def __is_substantivo_proprio(self, frase, palavra, *args):
        return bool(palavra.is_substantivo_proprio())
