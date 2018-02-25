# -*- coding: utf-8 -*-
"""
@project ensepro
@since 25/02/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import sys
import os
sys.path.append(os.path.abspath("../../"))

import ensepro

frases = [
    "Já fez alguma coisa que teve vontade de sair gritando na rua?"
]


def __command(frase_analisada, *args):
    ensepro.frase_pretty_print(frase_analisada, file=args[0]["file"])
    print("#" * 150, file=args[0]["file"], end="\n\n")


def carregar_frases():
    global frases
    frases = []
    with open("../../arquivos/frases/frases.txt", encoding="UTF-8") as frases_in_text:
        for frase in frases_in_text:
            frase = frase.replace("\n", "")

            if not frase:
                continue

            if frase.startswith("#"):
                continue

            frases.append(frase)


ensepro.analisar_frases_and_execute(frases, __command, file=None)
