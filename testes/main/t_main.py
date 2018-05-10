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
    return ensepro_path

sys.path.append(ensepro_path())

import ensepro
import json

frases = [
    "Qual é o nome completo de Abraham_lincoln?",
    "Quem é a esposa do presidente americano Abraham_lincoln?",
    "Qual é o maior lago da America_latina?",
    "Qual é o pais mais populoso da America_latina?",
    "Qual é o local de nascimento de Augusta_treveroro?"
    # "Quem é o presidente do Egito?"
]


frases_analisada = ensepro.analisar_frases(frases)
for frase_analisada in frases_analisada:
    ensepro.frase_pretty_print(frase_analisada, sinonimos=True)
# print(json.dumps(frase_analisada, indent=4, sort_keys=False), file=open("../../frase.json", mode="w", encoding="UTF-8"))



