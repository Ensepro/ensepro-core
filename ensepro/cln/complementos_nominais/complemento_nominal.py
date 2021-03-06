# -*- coding: utf-8 -*-
"""
@project ensepro
@since 25/02/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
from ensepro.conversores import make_json_serializable


class ComplementoNominal:

    def __init__(self, nome, complemento):
        self.nome = nome
        self.complemento = complemento

    @property
    def ok(self):
        return bool(self.nome) and bool(self.complemento)

    @property
    def as_text(self):
        return "{0} + {1}".format(self.nome.palavra_original, self.complemento.palavra_original)

    def __to_json__(self):
        return self.__dict__

    def __str__(self):
        return "ComplementoNominal{{nome={0}, complemento={1}}}" \
               "".format(self.nome, self.complemento)

    def __repr__(self):
        return self.__str__()
