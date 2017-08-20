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
REGEX_PALAVRA_RELEVANTE = re.compile(configuracoes.getRegexPalavraVerbo()+"|"+configuracoes.getRegexPalavraRelevante())
