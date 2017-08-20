"""
@project ensepro
@since 15/08/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import configuracoes
import json
import nlu
from servicos import PalavrasService as palavras
from bean.Frase import Frase
from utils import StringUtil
from constantes.StringConstantes import UTF_8
from constantes.StringConstantes import FILE_READ_ONLY
from constantes.StringConstantes import BREAK_LINE
from constantes.NLUConstantes import TIPO_FRASE
from constantes.NLUConstantes import LOCUCAO_VERBAL
from constantes.NLUConstantes import VOZ_ATIVA

frases = open(configuracoes.getPathArquivoFrases(), FILE_READ_ONLY, encoding=UTF_8).read().split(BREAK_LINE)
frases = [frase for frase in frases if not frase.startswith("#") and not StringUtil.isEmpty(frase)]

frasesAgrupadasPorTipo = {}
frasesAgrupadasPorLocucaoVerbal = {}
frasesAgrupadasPorVoz = {}

listaFrases = []

i = 0
for fraseTexto in frases:
    i += 1
    print(i)

    fraseAnalisada = palavras.analisarFrase(fraseTexto)

    if (not fraseAnalisada.ok):
        raise Exception("Falha na chamada do serviço de analise da frase(status_code=" + str(fraseAnalisada.status_code) + ")")

    jsonFrase = json.loads(fraseAnalisada.content)
    frase = Frase.fraseFromJson(jsonFrase)

    listaFrases.append(
        {
            "fraseTexto": fraseTexto,
            "frase": frase
        }
    )

    fraseProcessada = nlu.processarFrase(frase)

    if str(fraseProcessada[TIPO_FRASE]["tipo_palavra"]) not in frasesAgrupadasPorTipo:
        frasesAgrupadasPorTipo[str(fraseProcessada[TIPO_FRASE]["tipo_palavra"])] = []

    if str(fraseProcessada[LOCUCAO_VERBAL]["possui"]) not in frasesAgrupadasPorLocucaoVerbal:
        frasesAgrupadasPorLocucaoVerbal[str(fraseProcessada[LOCUCAO_VERBAL]["possui"])] = []

    if str(fraseProcessada[VOZ_ATIVA]) not in frasesAgrupadasPorVoz:
        frasesAgrupadasPorVoz[str(fraseProcessada[VOZ_ATIVA])] = []

    frasesAgrupadasPorTipo[str(fraseProcessada[TIPO_FRASE]["tipo_palavra"])].append(fraseTexto)
    frasesAgrupadasPorLocucaoVerbal[str(fraseProcessada[LOCUCAO_VERBAL]["possui"])].append(fraseTexto)
    frasesAgrupadasPorVoz[str(fraseProcessada[VOZ_ATIVA])].append(fraseTexto)

print("\n")
print("######################################################################################################")
print("                                     TIPOS ")
print("######################################################################################################")
print("\n")

print("===============================================================================")
for tipo in frasesAgrupadasPorTipo:
    print("Tipo: " + str(tipo) + "")
    print("-----------------------------------------------------------------------------")
    for fraseF in frasesAgrupadasPorTipo[tipo]:
        print("Frase: " + str(fraseF))
    print("===============================================================================")

print("\n")
print("######################################################################################################")
print("                                     LOCUÇÃO VERBAL ")
print("######################################################################################################")
print("\n")

print("===============================================================================")
for tipo in frasesAgrupadasPorLocucaoVerbal:
    print("Locução Verbal: " + str(tipo) + "")
    print("-----------------------------------------------------------------------------")
    for fraseF in frasesAgrupadasPorLocucaoVerbal[tipo]:
        print("Frase: " + str(fraseF))
    print("===============================================================================")

print("\n")
print("######################################################################################################")
print("                                     VOZ ")
print("######################################################################################################")
print("\n")

print("===============================================================================")
for tipo in frasesAgrupadasPorVoz:
    print("Voz: " + ("Ativa" if str(tipo) == "True" else "Passiva") + "")
    print("-----------------------------------------------------------------------------")
    for fraseF in frasesAgrupadasPorVoz[tipo]:
        print("Frase: " + str(fraseF))
    print("===============================================================================")



print("\n\n")

for frase in listaFrases:
    print("\n----------------------------------------------")
    print(frase["fraseTexto"])
    print(frase["frase"].obterPalavrasRelevantes())








