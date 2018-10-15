# -*- coding: utf-8 -*-
"""
@project ensepro
@since 20/09/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import json
from ensepro import configuracoes
from ensepro.constantes import ConfiguracoesConstantes, StringConstantes, LoggerConstantes

logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_NOMINALIZACAO)
nominalizacoes = json.loads(open(
    file=ConfiguracoesConstantes.ENSEPRO_PATH + configuracoes.get_config(ConfiguracoesConstantes.ARQUIVO_NOMINALIZACAO),
    mode=StringConstantes.FILE_READ_ONLY,
    encoding=StringConstantes.UTF_8
).read())


def get(verbo: str):
    logger.info("Obtendo nominalização do verbo: %s", verbo)
    result = nominalizacoes.get(verbo, [])
    logger.debug("Nominalizações: %s", str(result))
    return result
