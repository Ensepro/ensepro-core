"""
@project ensepro
@since 24/01/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import json
from ensepro.servicos import palavras_service
from ensepro.conversores import frase_conversor


# frase = "Você consegue imaginar o que poderia estar errado?"
frase = "Qual é a idade de Alencar?"

frase_analisada = palavras_service.analisar_frase(frase)
if (not frase_analisada.ok):
    print(frase_analisada)
    exit(1)

frase = frase_conversor.from_json(1, frase_analisada.json())

print(frase.id)
print(frase.palavras)
print(frase.arvore)
print(frase.tipo)
print(frase.voz)
print(frase.locucao_verbal)
print(frase.complementos_nominais)
# print(frase.arvore.to_nltk_tree().pretty_print())

# print(json.dumps(frase, ensure_ascii=False, indent=4, sort_keys=False))
