"""
@project ensepro
@since 24/01/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import ensepro

frase_text = "O mundo está nas mãos daqueles que têm a coragem de sonhar e de correr o risco de viver seus sonhos?"

frase = ensepro.analisar_frase(frase_text)

print("Frase id={}".format(frase.id))
print("Frase tipo={}".format(frase.tipo))
print("Frase voz={}".format(frase.voz))
print("Frase locucao_verbal={}".format(frase.locucao_verbal))
print("Frase complementos_nominais={}".format(frase.complementos_nominais))
print(frase.arvore.to_nltk_tree().pretty_print())
