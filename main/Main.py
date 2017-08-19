"""
@project ensepro
@since 20/07/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import sparql
import sys
import configuracoes
import json
import nlu
from servicos import PalavrasService as palavras
from bean.Frase import Frase
from utils import StringUtil
from constantes.StringConstantes import UTF_8
from constantes.StringConstantes import FILE_READ_ONLY
from constantes.StringConstantes import BREAK_LINE
from constantes.NLUConstantes import PALAVRAS_RELEVANTES
from constantes.TipoFrasesConstantes import TIPO_FRASE

frases = open(configuracoes.getPathArquivoFrases(), FILE_READ_ONLY, encoding=UTF_8).read().split(BREAK_LINE)
frases = [frase for frase in frases if not frase.startswith("#") and not StringUtil.isEmpty(frase)]

FRASE_ID = 0

frasesAgrupadas = {}
for fraseTexto in frases:
    FRASE_ID += 1
    fraseAnalisada = palavras.analisarFrase(fraseTexto)

    if (not fraseAnalisada.ok):
        raise Exception("Falha na chamada do serviço de analise da frase(status_code=" + str(fraseAnalisada.status_code) + ")")

    jsonFrase = json.loads(fraseAnalisada.content)
    frase = Frase.fraseFromJson(jsonFrase)

    if (not frase.isQuestao()):
        tipoFrase = frase.obterTipoFrase()[TIPO_FRASE]
        if (tipoFrase != "consulta"):
            break

    fraseProcessada = nlu.processarFrase(frase)

    palavrasRelevantes = ""
    for palavra in fraseProcessada[PALAVRAS_RELEVANTES]:
        palavrasRelevantes += palavra.palavraOriginal + " -- "


        print("Frase "+str(FRASE_ID)+": " + fraseTexto)
        # print("Palavras Relevantes:|>  " + palavrasRelevantes)
        # print("-------------------------------------------------------------------------------------------\n")


        with open("../__ignorar/frase" + str(FRASE_ID) + ".json", 'w', encoding=UTF_8) as out:
            out.write(json.dumps(frase, ensure_ascii=False, indent=4))




        # sparql.consular(fraseProcessada)
