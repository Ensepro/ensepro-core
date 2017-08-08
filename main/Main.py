"""
@project ensepro
@since 20/07/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import sparql
import json
import nlu
from servicos import Palavras as palavras
from bean.Frase import Frase

# fraseTexto = "quais doutorandos estão trabalhando na CWI?"
# fraseTexto = "quais são as tecnologias que foram produzidas pelo SemanTIC?"
fraseTexto = "tem algum doutorando no SemanTIC?"
# fraseTexto = "quem é Alencar?"

print("\nFrase a ser analisada: " + fraseTexto + "\n")


fraseAnalisada = palavras.analisarFrase(fraseTexto)

if(not fraseAnalisada.ok):
    raise Exception("Falha na chamada do serviço de analise da frase(status_code="+str(fraseAnalisada.status_code)+")")

jsonFrase = json.loads(fraseAnalisada.content)
frase = Frase.fraseFromJson(jsonFrase)

for palavra in frase.palavras:
    palavra.getSinonimos()

fraseProcessada = nlu.processarFrase(frase)

with open("../__ignorar/frase.json", 'w', encoding="utf8") as out:
    out.write(json.dumps(frase, ensure_ascii=False, indent=4))

sparql.consular(fraseProcessada)


