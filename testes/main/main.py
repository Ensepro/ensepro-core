# -*- coding: utf-8 -*-
"""
@project ensepro
@since 25/02/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import sys

def ensepro_path():
    import os
    # Obtém o PATH para a pasta que contém este arquivo
    this_file_directory = os.path.dirname(os.path.abspath(__file__))

    # Volta duas pastas
    ensepro_path = os.path.dirname(this_file_directory)
    ensepro_path = os.path.dirname(ensepro_path)
    print(ensepro_path)
    return ensepro_path

sys.path.append(ensepro_path())

import ensepro

frases = [
    "Já fez alguma coisa que teve vontade de sair gritando na rua?"
    # "Quem é o presidente do Egito?"
]



def __command(frase_analisada, *args):
    ensepro.frase_pretty_print(frase_analisada, file=args[0]["file"], print_sinonimos=True)
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
