"""
@project ensepro
@since 17/10/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""


from utils.StringUtil import remove_accentuation, has_accentuation

QUERY = {
            "query": {
                "query_string" : {
                    "fields" : [],
                    "query" : ""
                }
            }
        }



class QueryBuilder(object):

    def __init__(self):
        self.fields = []
        self.values = []


    def add_field(self, field):
        self.fields.append(field)
        return self

    def remove_field(self, field):
        if field in self.fields:
            self.fields.remove(field)

    def add_value(self, value):
        if(has_accentuation(value)):
            value = remove_accentuation(value)
        self.values.append(value.lower())
        return self

    def remove_value(self, field):
        if field in self.fields:
            self.fields.remove(field)

    def clear_values(self):
        self.values.clear()
        return self

    def clear_fields(self):
        self.fields.clear()
        return self

    def __format_values(self):

        format = "*{}* OR "


        val = ""
        for value in self.values:
            val += format.format(value)

        return val[:-4]

    def buildQuery(self):
        formated_values = self.__format_values()

        QUERY["query"]["query_string"]["fields"] = self.fields
        QUERY["query"]["query_string"]["query"] = formated_values

        return QUERY

    def __str__(self):
        return "QueryBuilder{fields="+str(self.fields)+", values="+str(self.values)+"}"

