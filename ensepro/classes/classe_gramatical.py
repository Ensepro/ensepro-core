# -*- coding: utf-8 -*-
"""
@project ensepro
@since 28/02/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
from enum import Enum
from ensepro.conversores import make_json_serializable
# TODO revisar valores
# http://www.nltk.org/_modules/nltk/corpus/reader/wordnet.html
#
# { Part-of-speech constants
# ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'
# }

class ClasseGramatical(Enum):
    VERBO = "v"
    ADJETIVO = "a"
    SUBSTANTIVO = "n"
    PREPOSICAO = "r"
    ADJ_SAT = "s"

    def __to_json__(self):
        return str(self)

    @classmethod
    def classe_gramatical_palavra(self, palavra):
        if palavra.is_verbo():
            return ClasseGramatical.VERBO
        if palavra.is_substantivo():
            return ClasseGramatical.SUBSTANTIVO
        if palavra.is_adjetivo():
            return ClasseGramatical.ADJETIVO
        if palavra.is_preposicao():
            return ClasseGramatical.PREPOSICAO
        return None