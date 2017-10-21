"""
@project ensepro
@since 17/10/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from utils.StringUtil import remove_accentuation, has_accentuation
from utils.LogUtil import error

QUERY = {
            "size": 10000,
            "query": {
                "query_string": {
                    "query": ""
                }
            }
        }


class QueryBuilder(object):
    def __init__(self):
        self.values = {}

    def __normalize(self, value):
        if has_accentuation(value):
            value = remove_accentuation(value)

        return value.lower()

    def add_field(self, field):
        field = self.__normalize(field)

        if field in self.values:
            error("QueryBuilder - Erro ao adicionar novo campo. Campo já existente[{}].".format(field))
            return

        self.values[field] = []
        return self

    def remove_field(self, field):
        if field in self.values:
            self.values.pop(field, None)

    def add_value(self, field, value):
        field = self.__normalize(field)
        value = self.__normalize(value)

        if field in self.values:
            self.values[field].append(value)
        else:
            error("QueryBuilder - Erro ao adicionar novo valor. Campo não existente[{}]".format(field))

        return self

    def remove_value(self, field, value):
        field = self.__normalize(field)
        value = self.__normalize(value)

        if field in self.values:
            if value in self.values[field]:
                self.values[field].remove(value)

    def clear_values(self, field):
        if field in self.values:
            self.values[field] = []
        return self

    def clear_fields(self):
        self.values = {}
        return self

    def __build_field_query(self, field):
        field_query = "{field}:({query})"

        query = self.values[field][0]
        for value in self.values[field][1:]:
            query += " OR {}".format(value)

        return field_query.format(field=field, query=query)

    def __build_query(self):

        query = ""
        for field in self.values:
            query += " {} AND".format(self.__build_field_query(field))

        #remove last " AND" from string
        return query[:-4]

    def buildQuery(self):
        if not self.values:
            error("QueryBuilder - Falha ao criar query. Fields e Values não pode estar vazio.")
            return None

        query = self.__build_query()

        QUERY["query"]["query_string"]["query"] = query

        return QUERY

    def __str__(self):
        return "QueryBuilder{{{}}}".format(str(self.values))
