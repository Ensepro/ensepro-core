"""
@project ensepro
@since 14/11/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""


def get(frase):
    pass


def __dn_prop(frase, palavra):
    pass


def __dn_adj(frase, palavra):
    pass


def __dn_num(frase, palavra):
    pass


def __dn_np(frase, palavra):
    pass


def __dn_pp(frase, palavra):
    pass


NUCLEOS = ["H:n", "H:prop"]
LOGICAS = {
    "DN:prop": __dn_prop,
    "DN:adj": __dn_adj,
    "DN:num": __dn_num,
    "DN:np": __dn_np,
    "DN:pp": __dn_pp,
}
