"""
@project ensepro
@since 10/08/2017
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


frases = open(configuracoes.getPathArquivoFrases(), FILE_READ_ONLY, encoding=UTF_8).read().split(BREAK_LINE)
frases = [frase for frase in frases if not frase.startswith("#") and not StringUtil.isEmpty(frase)]

frasesAgrupadas = {}
i = 0
for fraseTexto in frases:
    i+=1
    print(i)

    fraseAnalisada = palavras.analisarFrase(fraseTexto)

    if(not fraseAnalisada.ok):
        raise Exception("Falha na chamada do serviço de analise da frase(status_code="+str(fraseAnalisada.status_code)+")")

    jsonFrase = json.loads(fraseAnalisada.content)
    frase = Frase.fraseFromJson(jsonFrase)

    # frase.obterTipoFrase()
    # break
    # for palavra in frase.obterPalavrasComPalavraOriginalNaoVazia():
    #     palavra.getSinonimos()

    fraseProcessada = nlu.processarFrase(frase)

    # print("Tipo: "+str(fraseProcessada[TIPO_FRASE]))

    if str(fraseProcessada[TIPO_FRASE]["tipo_palavra"]) not in frasesAgrupadas:
        frasesAgrupadas[str(fraseProcessada[TIPO_FRASE]["tipo_palavra"])] = []

    frasesAgrupadas[str(fraseProcessada[TIPO_FRASE]["tipo_palavra"])].append(fraseTexto)

    # with open("../__ignorar/frase.json", 'w', encoding="utf8") as out:
    #     out.write(json.dumps(frase, ensure_ascii=False, indent=4))

    # sparql.consular(fraseProcessada)



print("===============================================================================")
for tipo in frasesAgrupadas:
    print("Tipo: " + str(tipo) + "")
    print("-----------------------------------------------------------------------------")
    for fraseF in frasesAgrupadas[tipo]:
        print("Frase: "+str(fraseF))
    print("===============================================================================")