"""
@project ensepro
@since 08/05/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
from ensepro.consulta.fields import Field
from ensepro.elasticsearch.searches import full_match_serach, parcial_match_search


DELIMITER = "_"

fields_full_match = [
    Field.FULL_MATCH_SUJEITO,
    Field.FULL_MATCH_PREDICADO,
    Field.FULL_MATCH_OBJETO,
]

fields_partial_match = [
    Field.PARTIAL_MATCH_SUJEITO,
    Field.PARTIAL_MATCH_PREDICADO,
    Field.PARTIAL_MATCH_OBJETO
]


def busca_no_elasticsearch_full(substantivo_comum):
    search_result = full_match_serach(fields_full_match, substantivo_comum.lower())
    if search_result["keys"]:
        return search_result

def busca_no_elasticsearch_partial(substantivo_comum):
    search_result = parcial_match_search(fields_partial_match, substantivo_comum.lower())
    if search_result["keys"]:
        return search_result


class ReferenciasSubstantivosComuns:

    def __init__(self, frase):
        self.frase = frase

    def localizar(self):
        substantivos_comuns = self.__list_substantivo_comum()
        if not substantivos_comuns:
            return None

        result_substantivo_comum = {}

        return result_substantivo_comum

    def __list_substantivo_comum(self):
        return self.frase.get_palavras(self.__is_substantivo_comum)

    def __is_substantivo_comum(self, frase, palavra, *args):
        return bool(palavra.is_substantivo())





