"""
@project ensepro
@since 20/01/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import json
from ensepro.servicos import palavras_service
from ensepro.conversores import frase_conversor


frase = "ser ser ou não ser ser"


frase_analisada = palavras_service.analisar_frase(frase)
if (not frase_analisada.ok):
    print(frase_analisada)
    exit(1)

frase = frase_conversor.from_json(1, frase_analisada.json())

print(frase.id)
print([str(palavra) for palavra in frase.palavras])
print(frase.arvore)
# print(frase.tipo)
print(frase.voz)
print(frase.locucao_verbal)
# print(frase.complementos_nominais)
# print(frase)

print(json.dumps(frase, ensure_ascii=False, indent=4, sort_keys=False))
