"""
@project ensepro
@since 25/01/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""


class ComplementoNominal:

    def __init__(self, nome, complemento):
        self.nome = nome
        self.complemento = complemento

    @property
    def ok(self):
        return bool(self.nome) and bool(self.complemento)

    def __str__(self):
        return "ComplementoNominal{{nome={0}, complemento={1}}}" \
               "".format(self.nome, self.complemento)

    def __repr__(self):
        return self.__str__()
