"""
@project ensepro
@since 17/10/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""


QUERY = {
            "size": 10000,
            "query": {
                "regexp": {

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
        self.values.append(value)
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

    def __createRegex(self):
        val = ""
        for value in self.values[:2]:
            val += "|.*{}.*".format(value)

        return val[1:]+"|.*fernando_correia_dias.*"

    def buildQuery(self):
        #TODO REVIEW ao utilizar a query de regex, com muitas condições, o ES não consegue determinar os resultados finais
        # Devido a muitos estados
        QUERY["query"]["regexp"][self.fields[0]] =  self.__createRegex()

        return str(QUERY).replace("'", "\"")


    def __str__(self):
        return "QueryBuilder{fields="+str(self.fields)+", values="+str(self.values)+"}"

