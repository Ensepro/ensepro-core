"""
@project ensepro
@since 20/07/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import nlu
from servicos import Palavras as palavras
from bean.Frase import Frase
import json

# fraseTexto = "quais doutorandos estão trabalhando na CWI?"
fraseTexto = "quais são as tecnologias que foram produzidas pelo SemanTIC?"

print("\nFrase a ser analisada: " + fraseTexto + "\n")


fraseAnalisada = palavras.analisarFrase(fraseTexto)

if(not fraseAnalisada.ok):
    raise Exception("Falha na chamada do serviço de analise da frase(status_code="+str(fraseAnalisada.status_code)+")")

jsonFrase = json.loads(fraseAnalisada.content)
frase = Frase.fraseFromJson(jsonFrase)

fraseProcessada = nlu.processarFrase(frase)

# print(fraseProcessada)
for palavra in frase.palavras:
    palavra.getSinonimos()

for info in fraseProcessada:
    print(str(info) + ": " + str(fraseProcessada[info]))




# print(json.dumps(frase, ensure_ascii=False, indent=2))