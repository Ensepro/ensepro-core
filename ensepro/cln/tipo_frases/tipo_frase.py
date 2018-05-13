# -*- coding: utf-8 -*-
"""
@project ensepro
@since 25/02/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
from ensepro.conversores import make_json_serializable


class TipoFrase:

    def __init__(self, bot_response=None, ids=list()):
        self.tipo = bot_response.text if bot_response else None
        self.confianca = bot_response.confidence if bot_response else None
        self.ids = ids

    def __str__(self):
        return "TipoFrase={{tipo={0}, confianca={1}, ids={2}}}".format(self.tipo, self.confianca, self.ids)

    def __to_json__(self):
        return self.__dict__
