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
from ensepro.consulta import ReferenciasSubstantivosProprios

# frase = "Obtenha a imagem de Anatole france."
frase = "Obtenha uma imagem da Angola."
# frase = "Obtenha uma imagem de Heisenberg."
# frase = "Obtenha uma imagem de Charles Darwin."
# frase = "Obtenha uma imagem da batalha de Gettysburg."
# frase = "Quem é o apresentador do BBC Wildlife Specials"
# frase = "Quantas cadeiras tem o estádio de Futebol do Clube do Porto?"


args = sys.argv
# frase = sys.argv[1]

print_dados = False
if len(sys.argv) > 2:
    print_dados = sys.argv[2] == "-p"

frase_processada = ensepro.analisar_frase(frase)
if print_dados or True:
    ensepro.frase_pretty_print(frase_processada)

referencias = ReferenciasSubstantivosProprios(frase_processada)
result = referencias.localizar()
print(result)
