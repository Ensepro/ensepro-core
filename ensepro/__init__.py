# -*- coding: utf-8 -*-
"""
@project ensepro
@since 25/02/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

# Modulos/classes/funções publicas na importação
from ensepro.classes import *
from ensepro.constantes import *

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


def frase_pretty_print(frase: Frase,
                       file=None,
                       termos_relevantes=False,
                       sinonimos=False,
                       complementos_nominais=False,
                       locucoes_verbais=False,
                       tags=False,
                       arvore=False,
                       verbose=False):
    if not isinstance(frase, Frase):
        raise Exception("Não é um objeto Frase.")

    print("-> Frase {0}: {1}".format(frase.id, frase.frase_original), file=file)
    print("--> Tipo:", frase.tipo, file=file)
    print("--> Voz:", frase.voz, file=file)

    if termos_relevantes or verbose:
        print("--> Termos Relevantes:", file=file)
        if frase.palavras_relevantes:
            for index, palavra in enumerate(frase.palavras_relevantes):
                print("----> TR {0}:".format(index), palavra, file=file)
                if sinonimos or verbose:
                    print("--------> Sinonimos: " + str(palavra.sinonimos), file=file)
        else:
            print("----> Nenhuma.", file=file)

    if complementos_nominais or verbose:
        print("--> Complementos Nominais:", file=file)
        if frase.complementos_nominais:
            for index, cn in enumerate(frase.complementos_nominais):
                print("----> CN {0}:".format(index), cn.as_text, file=file)
        else:
            print("----> Nenhum.", file=file)

    if locucoes_verbais or verbose:
        print("--> Locuções Verbais:", file=file)
        if frase.locucao_verbal:
            for index, lv in enumerate(frase.locucao_verbal):
                print("----> LV {0}:".format(index), lv, file=file)
        else:
            print("----> Nenhum.", file=file)

    if tags or verbose:
        print("--> Tags das palavras", file=file)
        for palavra in frase.palavras:
            print("Palavra[{:>3}] {:>20} - {:>20}: {}".format(palavra.id, palavra.palavra_original, palavra.palavra_canonica, str(palavra.tags)),
                  file=file)

    if arvore or verbose:
        frase.arvore.to_nltk_tree().pretty_print(stream=file)


def save_as_json(value, filename, indent=4, sort_keys=False):
    import json
    print(
            json.dumps(value, indent=indent, sort_keys=sort_keys, ensure_ascii=False),
            file=open(filename, mode='w', encoding="UTF-8")
    )
