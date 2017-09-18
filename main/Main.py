"""
@project ensepro
@since 20/07/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import sys
import configuracoes
import json
import nlu
import sparql
from servicos import PalavrasService as palavras
from bean.Frase import Frase
from utils import StringUtil
from utils import FraseTreeUtil
from constantes.ConfiguracoesConstantes import SAVE_FILES_TO
from constantes.StringConstantes import UTF_8
from constantes.StringConstantes import FILE_READ_ONLY
from constantes.StringConstantes import FILE_WRITE_ONLY
from constantes.StringConstantes import BREAK_LINE
from constantes.NLUConstantes import PALAVRAS_RELEVANTES
from constantes.TipoFrasesConstantes import TIPO_FRASE

"""
-m "{frase}"  -> frase a ser analisada  
-tree         -> cria um arquivo com a árvore desenhada.
"""

frases = []
params = {}


def loadParams():
    params["frase"] = "-m" in sys.argv
    if (params["frase"]):
        frases.append(sys.argv[sys.argv.index("-m") + 1])

    params["tree"] = "-tree" in sys.argv


loadParams()
if not params["frase"]:
    frases = open(configuracoes.getPathArquivoFrases(), FILE_READ_ONLY, encoding=UTF_8).read().split(BREAK_LINE)
    frases = [frase for frase in frases if not frase.startswith("#") and not StringUtil.isEmpty(frase)]

FRASE_ID = 0
print("-------------------------------------------------------------------------------------------\n")
frasesAgrupadas = {}
for fraseTexto in frases:
    FRASE_ID += 1
    FRASE_NAME = "frase" + str(FRASE_ID)
    print("MAIN - Frase: " + fraseTexto)

    print("MAIN - Executando analise do Palavras...")
    fraseAnalisada = palavras.analisarFrase(fraseTexto)

    if (not fraseAnalisada.ok):
        raise Exception("Falha na chamada do serviço de analise da frase(status_code=" + str(fraseAnalisada.status_code) + ")")

    print("MAIN - Frase analisada pelo Palavras.")
    jsonFrase = fraseAnalisada.json()
    frase = Frase.fraseFromJson(jsonFrase)

    if (not frase.isQuestao()):
        tipoFrase = frase.obterTipoFrase()[TIPO_FRASE]
        if (tipoFrase != "consulta"):
            print("MAIN - Frase não é uma pergunta e nem do tipo 'consulta'!")
            continue

    print("MAIN - Executando NLU")
    fraseProcessada = nlu.processarFrase(frase)

    print("MAIN - Preparando print...")
    palavrasRelevantes = ""
    for palavra in fraseProcessada[PALAVRAS_RELEVANTES]:
        palavrasRelevantes += palavra.palavraOriginal + " -- "

    print("\n-------------------------------------------------------------------------------------------")
    print("Frase " + str(FRASE_ID) + ": " + fraseTexto)
    print("Palavras Relevantes:|>  " + str(palavrasRelevantes))
    print("Voz Ativa:|>  " + str(frase.isVozAtiva()))
    print("Locução Verbal:|>  " + str(frase.possuiLocucaoVerbal()))
    print("-------------------------------------------------------------------------------------------\n")

    print("MAIN - Executante consulta sparql....")
    sparql.consular(fraseProcessada, FRASE_ID)

    print("MAIN - Consulta sparql finalizada.")
    print("MAIN - Salvando informações em arquivo json....")

    fraseToJson = {}
    fraseToJson["fraseOriginal"] = fraseTexto
    fraseToJson["objetoFrase"] = frase

    with open(SAVE_FILES_TO + FRASE_NAME + ".json", FILE_WRITE_ONLY, encoding=UTF_8) as out:
        out.write(json.dumps(fraseToJson, ensure_ascii=False, indent=4, sort_keys=True))

    if (params["tree"]):
        print("MAIN - Gerando árvore...")
        FraseTreeUtil.printTreeFormat(frase, SAVE_FILES_TO + FRASE_NAME + "_tree.txt")
        print("MAIN - Árvore gerada.")

    print("-------------------------------------------------------------------------------------------\n")
    # if(FRASE_ID >= 1):
    #      break
