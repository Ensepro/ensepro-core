"""
@project ensepro
@since 17/10/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import nlu
import json
from constantes.ConfiguracoesConstantes import SAVE_FILES_TO
from constantes.StringConstantes import FILE_WRITE_ONLY
from constantes.TipoFrasesConstantes import TIPO_FRASE
from servicos import PalavrasService as palavras
from constantes.StringConstantes import UTF_8
from utils.LogUtil import error, debug, info
from utils import FraseTreeUtil
from bean.Frase import Frase
from utils import ElasticSearchUtil




class Ensepro(object):
    def __init__(self):
        self.__params = {}
        self.__frases = []

    def addFrase(self, frase):
        self.__frases.append(frase)

    def addParam(self, key, value):
        self.__params[key] = value

    def analisarFrase(self, frase, id):
        """
        Retorna um objeto Frase já com a frase analisada.
        :param frase: Frase no formato de texto
        :return: Frase
        """
        debug("Ensepro - Analisando frase: [{id} - \"{frase}\"]".format(id=id, frase=frase))

        fraseAnalisada = palavras.analisarFrase(frase)
        if (fraseAnalisada.ok):
            jsonFrase = fraseAnalisada.json()
            debug("Ensepro - frase analisada com sucesso ({})".format(jsonFrase))

            return Frase.fraseFromJson(jsonFrase, id)

        msg = "Falha na chamada do serviço de analise da frase(status_code={})".format(str(fraseAnalisada.status_code))
        error("Ensepro - " + msg)
        raise Exception(msg)

    def processarFrase(self, frase):
        debug("Ensepro - executando NLU para frase [id={}]".format(frase.id))
        return nlu.processarFrase(frase)

    def __isFraseValida(self, frase: Frase):
        return frase.isQuestao() or frase.obterTipoFrase()[TIPO_FRASE] == "consulta"

    def __printDadosFrase(self, frase : Frase):
        debug("Dados da frase: \n\t"
             "Frase: {fraseTexto}\n\t"
             "Palavras Relevantes: {relevantes}\n\t"
             "Voz Ativa: {voz}\n\t"
             "Locução Verbal: {locucao}\n"
                .format(
                    fraseTexto=self.__frases[frase.id-1],
                    relevantes=str(frase.obterPalavrasRelevantes()),
                    voz=str(frase.isVozAtiva()),
                    locucao=str(frase.possuiLocucaoVerbal())
                )
            )


    def __salvarFrase(self, frase : Frase):
        info("Ensepro - salvando dados da frase em arquivo json.")
        toJson = {}
        toJson["fraseOriginal"] = self.__frases[frase.id-1]
        toJson["frase"] = frase

        with open(SAVE_FILES_TO.format(fileName="frase{}.json".format(frase.id)), FILE_WRITE_ONLY, encoding=UTF_8) as out:
            out.write(json.dumps(toJson, ensure_ascii=False, indent=4, sort_keys=True))


    def executar(self):
        numFrases = len(self.__frases)
        info("Enspero - iniciando processamento das frases[{}].".format(numFrases))

        for index in range(numFrases):
            frase = self.analisarFrase(self.__frases[index], (index) + 1)

            if not self.__isFraseValida(frase):
                continue

            fraseProcessada = self.processarFrase(frase)

            self.__printDadosFrase(frase)

            self.__salvarFrase(frase)

            if (self.__params["tree"]):
                info("Ensepro - criando árvore gráfica da frase.")
                FraseTreeUtil.printTreeFormat(frase, SAVE_FILES_TO.format(fileName="frase{}_tree.txt.json".format(frase.id)))


            ElasticSearchUtil.consultar(fraseProcessada, frase.id)



