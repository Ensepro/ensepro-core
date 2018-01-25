"""
@project ensepro
@since 25/01/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""


class TipoFrase:

    def __init__(self, bot_response=None):
        self.tipo = bot_response.text if bot_response else None
        self.confianca = bot_response.confidence if bot_response else None

    def __str__(self):
        return "TipoFrase={{tipo={0}, confianca={1}}}".format(self.tipo, self.confianca)
