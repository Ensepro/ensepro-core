"""
@project ensepro
@since 09/03/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
from ensepro.elasticsearch.queries import Query, SimpleQuerySearch
from ensepro.elasticsearch import connection
from .search import execute_search


def  simple_search(field_search, value_search):
    simple_query = SimpleQuerySearch()
    simple_query.add_field(field_search)
    simple_query.add_value(value_search)
    query = Query.build_default(simple_query.build_query())
    return execute_search(connection(), query)
