"""
@project ensepro
@since 19/01/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
from enum import Enum
from ensepro.conversores import make_json_serializable


class Frase:
    def __init__(self, id=None, palavras=None):
        self.id = id
        self.palavras = palavras
        self.__tipo = None
        self.__locucao_verbal = None
        self.__palavras_relevantes = None
        self.__voz = None
        self.__complementos_nominais = None

    @property
    def tipo(self):
        # TODO obter o tipo antes de retornar
        # if self.__tipo:
        #     return self.__tipo
        # self.__tipo = get_tipo_1234_1234(self)
        return self.__tipo

    @property
    def locucao_verbal(self):
        # TODO verificar existencia de locucao verbal antes de retornar
        # if self.__locucao_verbal:
        #     return self.__locucao_verbal
        # self.__locucao_verbal = get_locucao_verbal_1234_1234()
        return self.__locucao_verbal

    @property
    def palavras_relevantes(self):
        # TODO determinar palavras relevantes antes de retornar
        # if self.__palavras_relevantes:
        #     return self.__palavras_relevantes
        # self.__palavras_relevantes = obtem_palavras_relevantes(self)
        return self.__palavras_relevantes

    @property
    def voz(self):
        # TODO determinar se é voz ativa ou passiva antes de retornar
        # if self.__voz:
        #     return self.__voz
        # self.__voz = get_voz(self)
        return self.__voz

    @property
    def complementos_nominais(self):
        # TODO buscar complementações nominais antes de retornar
        # if self.__complementos_nominais:
        #     return self.__complementos_nominais
        # self.__complementos_nominais = get_complementos_nominais(self)
        return self.__complementos_nominais

    def to_json(self):
        return self.__dict__

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return str(self) == str(other)

    def __str__(self):
        return \
            "Frase={{id={0}, palavras={1}, tipo={2}, locucao_verbal={3}, voz={4}}}" \
            "".format(
                    str(self.id),
                    str(self.palavras),
                    str(self.tipo),
                    str(self.locucao_verbal),
                    str(self.voz)
            )


class VozType(Enum):
    ATIVA = 1
    PASSIVA = 2
