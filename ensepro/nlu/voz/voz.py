"""
@project ensepro
@since 21/01/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import re
from enum import Enum
from ensepro import configuracoes
from ensepro.constantes import ConfiguracoesConstantes, LoggerConstantes

regex_voz_passiva = re.compile(configuracoes.get_config(ConfiguracoesConstantes.REGEX_VOZ_PASSIVA))
logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_VOZ)


class Voz(Enum):
    PASSIVA = 'passiva'
    ATIVA = 'ativda'


def get(frase):
    logger.info("Obtendo voz da frase: [%s]", frase)

    for palavra in frase.palavras:
        logger.debug("Verificando palavras: [palavra.tag_inicial=%s, regex=%s]", palavra.tag_inicial, regex_voz_passiva)

        if regex_voz_passiva.search(palavra.tag_inicial):
            logger.info("[%s] = %s", frase, Voz.PASSIVA)
            return Voz.PASSIVA

    logger.info("[%s] = %s", frase, Voz.ATIVA)
    return Voz.ATIVA
