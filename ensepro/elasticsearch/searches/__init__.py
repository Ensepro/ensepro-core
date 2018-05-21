"""
@project ensepro
@since 09/03/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
from ensepro.constantes import LoggerConstantes
from ensepro.elasticsearch import connection
from ensepro.elasticsearch.queries import Query, QueryStringSearch, QueryTermSearch, QueryTermsSearch
from .search import execute_search

logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_ES_CONSULTA)


def simple_query_string_search(field, value):
    query_string = QueryStringSearch()
    query_string.add_field(field)
    query_string.add_value(value)
    query = Query.build_default(query_string.build_query())
    logger.info("Criando QueryString")
    return execute_search(connection(), query)


def simple_query_term_search(field, value):
    query_term = QueryTermSearch(field, value)
    query = Query.build_default(query_term.build_query())
    logger.info("Criando QueryTerm")
    return execute_search(connection(), query)


def simple_query_terms_search(field, values):
    query_term = QueryTermsSearch(field, values)
    query = Query.build_default(query_term.build_query())
    logger.info("Criando QueryTerms")
    return execute_search(connection(), query)


def search(fields, value, query):
    full_search_result = {}
    search_result_keys = ""
    logger.info("Executando busca: [fields=%s, value=%s]", fields, value)
    for field in fields:
        field_name = field.value["name"]
        field_key = field.value["key"]
        search_result = query(field_name, value)

        if search_result["hits"]["total"] > 0:
            full_search_result[field_name] = search_result
            search_result_keys += field_key

    return {
        "result": full_search_result,
        "keys": search_result_keys
    }


def full_match_serach(fields, value):
    return search(fields, value, simple_query_string_search)


def parcial_match_search(fields, value):
    return search(fields, value, simple_query_term_search)


def list_parcial_match_search(fields, values):
    return search(fields, values, simple_query_terms_search)
