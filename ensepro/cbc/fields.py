"""
@project ensepro
@since 07/05/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
from enum import Enum


def create_field(name, key):
    return {
        "name": name,
        "key": key
    }


class Field(Enum):
    FULL_MATCH_SUJEITO = create_field("sujeito.conceito", "S")
    FULL_MATCH_PREDICADO = create_field("predicado.conceito", "P")
    FULL_MATCH_OBJETO = create_field("objeto.conceito", "O")
    PARTIAL_MATCH_SUJEITO = create_field("sujeito.ngram_conceito", "s")
    PARTIAL_MATCH_PREDICADO = create_field("predicado.ngram_conceito", "p")
    PARTIAL_MATCH_OBJETO = create_field("objeto.ngram_conceito", "o")
