# -*- coding: utf-8 -*-
"""
@project ensepro
@since 09/05/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""


def carregar_frases(arquivo):
    frases = []
    with open(arquivo, mode="r", encoding="UTF-8") as frases_arquivo:
        for frase in frases_arquivo:
            frase = frase.replace("\n", "")
            if not frase:
                continue
            if frase.startswith("#"):
                continue
            frases.append(frase)

    return frases


def print_frase(ensepro, frase, args, file=None):
    ensepro.frase_pretty_print(
        frase,
        file=file,
        termos_relevantes=args.verbose or args.termos_relevantes,
        sinonimos=args.verbose or args.sinonimos,
        complementos_nominais=args.verbose or args.complementos_nominais,
        locucoes_verbais=args.verbose or args.locucoes_verbais,
        tags=args.verbose or args.tags,
        arvore=args.verbose or args.arvore
    )


def comparar_frases(ensepro, frase1, frase2, args, file=None):
    ensepro.comparar_frases(
        frase1,
        frase2,
        file=file,
        termos_relevantes=args.verbose or args.termos_relevantes,
        sinonimos=args.verbose or args.sinonimos,
        complementos_nominais=args.verbose or args.complementos_nominais,
        locucoes_verbais=args.verbose or args.locucoes_verbais,
        tags=args.verbose or args.tags,
        arvore=args.verbose or args.arvore
    )


def print_frases(ensepro, frases, args, file=None):
    for frase in frases:
        print_frase(ensepro, frase, args, file=file)


def print_resposta(ensepro, resposta, file=None):
    ensepro.resposta_pretty_print(resposta, file=file)
