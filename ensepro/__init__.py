"""
@project ensepro
@since 20/01/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

# Modulos/classes/funções publicas na importação
from .classes import *
from .arvore import *
from .sinonimos import *
from .constantes import *
from .nlu import *

__FRASE_ID = 0


def __next_id():
    global __FRASE_ID
    __FRASE_ID += 1
    return __FRASE_ID


def analisar_frase(frase: str):
    from ensepro.servicos import palavras_service
    from ensepro.conversores import frase_conversor

    logger = LoggerConstantes.default_logger()
    id = __next_id()
    try:
        logger.info("Iniciando processamento: [frase_id=%s, frase=%s]", id, frase)

        frase_analisada = palavras_service.analisar_frase(frase)
        frase_final = frase_conversor.from_json(id, frase_analisada.json())

        logger.info("Frase processada: [frase=%s]", frase_final)
        return frase_final
    except Exception as ex:
        logger.exception(ex)
        raise ex
