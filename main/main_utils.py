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


def print_frases(ensepro, frases, args, file=None):
    for frase in frases:
        ensepro.frase_pretty_print(
                frase,
                file=file,
                termos_relevantes=args.termos_relevantes,
                sinonimos=args.sinonimos,
                complementos_nominais=args.complementos_nominais,
                locucoes_verbais=args.locucoes_verbais,
                tags=args.tags,
                arvore=args.arvore,
                verbose=args.verbose

        )
