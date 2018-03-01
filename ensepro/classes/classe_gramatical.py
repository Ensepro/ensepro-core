# -*- coding: utf-8 -*-
"""
@project ensepro
@since 28/02/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
from enum import Enum

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