# -*- coding: utf-8 -*-
"""
@project ensepro
@since 25/02/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

# Modulos/classes/funções publicas na importação
from .classes import *
from .arvore import *
from .sinonimos import *
from .constantes import *
from .cln import *

__FRASE_ID = 0


def __next_id():
    global __FRASE_ID
    __FRASE_ID += 1
    return __FRASE_ID


def analisar_frases(frases: list) -> list:
    frases_analisadas = []
    for frase in frases:
        frases_analisadas.append(analisar_frase(frase))

    return frases_analisadas


def analisar_frases_and_execute(frases: list, command, **args):
    for frase in frases:
        frase_analisada = analisar_frase(frase)
        command(frase_analisada, args)


def analisar_frase(frase: str):
    from ensepro.servicos import palavras_service
    from ensepro.conversores import frase_conversor

    logger = LoggerConstantes.default_logger()
    id = __next_id()
    try:
        logger.info("Iniciando processamento: [frase_id=%s, frase=%s]", id, frase)

        frase_analisada = palavras_service.analisar_frase(frase)
        frase_final = frase_conversor.from_json(id, frase, frase_analisada.json())

        logger.info("Frase processada: [frase=%s]", frase_final)
        return frase_final
    except Exception as ex:
        logger.exception(ex)
        raise ex


def frase_pretty_print(frase: Frase, file=None):
    if not isinstance(frase, Frase):
        raise Exception("Não é um objeto Frase.")

    print("->Frase {0}: {1}".format(frase.id, frase.frase_original), file=file)
    print("--> Tipo:", frase.tipo, file=file)
    print("--> Voz:", frase.voz, file=file)
    print("--> Palavras Relevantes:", file=file)
    if frase.palavras_relevantes:
        for index, palavra in enumerate(frase.palavras_relevantes):
            print("----> PR {0}:".format(index), palavra, file=file)
    else:
        print("----> Nenhuma.", file=file)

    print("--> Complementos Nominais:", file=file)
    if frase.complementos_nominais:
        for index, cn in enumerate(frase.complementos_nominais):
            print("----> CN {0}:".format(index), cn.as_text, file=file)
    else:
        print("----> Nenhum.", file=file)

    print("--> Locuções Verbais:", file=file)
    if frase.locucao_verbal:
        for index, lv in enumerate(frase.locucao_verbal):
            print("----> LV {0}:".format(index), lv, file=file)
    else:
        print("----> Nenhum.", file=file)

    frase.arvore.to_nltk_tree().pretty_print(stream=file)
