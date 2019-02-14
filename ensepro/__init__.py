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


def comparar_frase(frase1: Frase, frase2: Frase,
                   file=None,
                   termos_relevantes=False,
                   sinonimos=False,
                   complementos_nominais=False,
                   locucoes_verbais=False,
                   tags=False,
                   arvore=False,
                   resposta=False):
    # TODO implementar
    print("Método ainda não implementado")

    pass


def frase_pretty_print(frase: Frase,
                       file=None,
                       termos_relevantes=False,
                       sinonimos=False,
                       complementos_nominais=False,
                       locucoes_verbais=False,
                       tags=False,
                       arvore=False):
    if not isinstance(frase, Frase):
        raise Exception("Não é um objeto Frase.")

    print("-> Frase {0}: {1}".format(frase.id, frase.frase_original), file=file)
    print("--> Tipo:", frase.tipo, file=file)
    print("--> Voz:", frase.voz, file=file)

    if termos_relevantes:
        print("--> Termos Relevantes:", file=file)
        if frase.termos_relevantes:
            for index, palavra in enumerate(frase.termos_relevantes):
                print("----> TR {0}:".format(index), palavra, file=file)
                if sinonimos:
                    print("--------> Sinonimos: " + str(palavra.sinonimos), file=file)
        else:
            print("----> Nenhuma.", file=file)

    if complementos_nominais:
        print("--> Complementos Nominais:", file=file)
        if frase.complementos_nominais:
            for index, cn in enumerate(frase.complementos_nominais):
                print("----> CN {0}:".format(index), cn.as_text, file=file)
        else:
            print("----> Nenhum.", file=file)

    if locucoes_verbais:
        print("--> Locuções Verbais:", file=file)
        if frase.locucao_verbal:
            for index, lv in enumerate(frase.locucao_verbal):
                print("----> LV {0}:".format(index), lv, file=file)
        else:
            print("----> Nenhum.", file=file)

    if tags:
        print("--> Tags das palavras", file=file)
        for palavra in frase.palavras:
            print("----> Palavra[{:>3}] {:>20} - {:<20}==> {}".format(palavra.id, palavra.palavra_original,
                                                                      palavra.palavra_canonica,
                                                                      str(palavra.tags)),
                  file=file)

    if arvore:
        frase.arvore.to_nltk_tree().pretty_print(stream=file)


def resposta_pretty_print(resposta, somente_resposta=False, file=None):
    if not resposta:
        print("Nenhuma resposta encontrada.\n", file=file)
        return

    if somente_resposta:
        list_all_triples = []
        for answer in resposta["correct_answer"]:
            for triple in answer["triples"]:
                list_all_triples.append(triple)

        list_all_triples = sorted(list_all_triples, key=lambda x: (
            x["subject"], x["predicate"], x["object"]
        ))

        for triple in list_all_triples:
            print(triple, end="")

        return

    import ensepro.configuracoes as configuracoes
    from ensepro import ConsultaConstantes
    resultado_resumido = configuracoes.get_config(ConsultaConstantes.RESULTADO_RESUMIDO)

    respostas = [resposta["correct_answer"], resposta["all_answers"]]

    for index, _resposta in enumerate(respostas):
        if (index == 0):
            print("\nMelhores respostas:", file=file)
        else:
            print("\nLista de triplas candidatas a resposta: ", file=file)

        for index, tripla in enumerate(_resposta):
            to_print = ["{0:.3f}".format(tripla["score"])]
            temp = []
            for value in tripla["triples"]:
                for key in value:
                    temp.append(str(value[key]))

            to_print.append("[" + ' | '.join(temp) + "]")
            to_print.append("-")
            if not resultado_resumido:
                temp = []
                for value in tripla["details"]["metrics"]["scoreMetrics"]:
                    temp.append("{0:.3f}".format(value))
                to_print.append("[" + ' '.join(temp) + "]")

                temp = []
                for value in tripla["details"]["metrics"]["metrics"]:
                    temp.append("{0:.2f}".format(value["weight"]) + "(" + value["policy"] + ")")
                # to_print.append("metricsClass: [" + ','.join(temp) + "]")

            print(str(index), ' '.join(to_print), file=file)


def save_as_json(value, filename, indent=4, sort_keys=False):
    import json
    print(
        json.dumps(value, indent=indent, sort_keys=sort_keys, ensure_ascii=False),
        file=open(filename, mode='w', encoding="UTF-8"),
        flush=True
    )
