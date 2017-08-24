"""
@project ensepro
@since 16/08/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import configuracoes
import re

INDICE_VALIDA_QUESTAO = 0
LOCUCAO_VERBAL_POSSUI = "possui"
LOCUCAO_VERBAL_VERBOS = "verbos"

REGEX_VOZ_PASSIVA = re.compile(configuracoes.getRegexVozPassiva())
REGEX_PALAVRA_VERBO = re.compile(configuracoes.getRegexPalavraVerbo())
REGEX_PALAVRA_ADJETIVO = re.compile(configuracoes.getRegexPalavraAdjetivo())
REGEX_PALAVRA_RELEVANTE = re.compile(configuracoes.getRegexPalavraVerbo()+"|"+configuracoes.getRegexPalavraRelevante())
REGEX_PALAVRA_PREPOSICAO = re.compile(configuracoes.getRegexPalavraPreposicao())
REGEX_PALAVRA_SUBSTANTIVO = re.compile(configuracoes.getRegexPalavraSubstantivo())




