"""
@project ensepro
@since 13/04/2018
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
from ensepro.consulta import ReferenciasSubstantivosProprios, ReferenciasSubstantivosComuns

# frase = "Obtenha o nome completo da mulher americana Anatole france."
# frase = "Obtenha uma imagem da Angola."
# frase = "Obtenha uma imagem de Heisenberg."
# frase = "Obtenha uma imagem de Charles Darwin."
# frase = "Obtenha uma imagem da batalha de Gettysburg."
# frase = "Quem é o apresentador do BBC Wildlife Specials"
# frase = "Quantas cadeiras tem o estádio de Futebol do Clube do Porto?"
# frase = "Quem é a esposa do presidente americano Anatole_france?"
# frase = "Qual é o clima da Argentina?"
# frase = "Quanto é o idh ano de Andorra"
# frase = "Qual é o maior lago da América latina?"
# frase = "Qual é o pais mais rico da América latina?"
# frase = "Qual é p numero de paises da América latina?"

frase = "Quem é a esposa do presidente americano Lincoln?"

args = sys.argv
# frase = sys.argv[1]

print_dados = False
if len(sys.argv) > 2:
    print_dados = sys.argv[2] == "-p"

frase_processada = ensepro.analisar_frase(frase)
if print_dados or True:
    ensepro.frase_pretty_print(frase_processada)

substantivos_proprios = ReferenciasSubstantivosProprios(frase_processada)
result_substantivos_proprios = substantivos_proprios.localizar()
print(json.dumps(result_substantivos_proprios, indent=4, sort_keys=False, ensure_ascii=False),
      file=open("substantivo_proprio.json", mode="w", encoding="UTF-8"))

for substantivo in result_substantivos_proprios:
    substantivo = result_substantivos_proprios[substantivo]
    if "nova_frase" in substantivo:
        frase = substantivo["nova_frase"]
        frase_processada = ensepro.analisar_frase(frase)
        ensepro.frase_pretty_print(frase_processada)
        break



substantivos_comuns = ReferenciasSubstantivosComuns(frase_processada)
result_substantivos_comuns = substantivos_comuns.localizar()


print(json.dumps(result_substantivos_comuns, indent=4, sort_keys=False, ensure_ascii=False),
      file=open("substantivo_comuns.json", mode="w", encoding="UTF-8"))
# print(result)
