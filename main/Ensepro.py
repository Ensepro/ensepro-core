"""
@project ensepro
@since 17/10/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import nlu
from constantes.ConfiguracoesConstantes import SAVE_FILES_TO
from constantes.TipoFrasesConstantes import TIPO_FRASE
from constantes.FraseConstantes import LOCUCAO_VERBAL_POSSUI, LOCUCAO_VERBAL_VERBOS
from servicos import PalavrasService as palavras
from utils.LogUtil import error, debug, info
from utils import FraseTreeUtil
from bean.Frase import Frase
from utils import ElasticSearchUtil
from utils.JsonUtil import save_to_json


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
             "Tipo: {tipoFrase}\n\t"
             "Palavras Relevantes: {relevantes}\n\t"
             "Voz Ativa: {voz}\n\t"
             "Locução Verbal: {locucao}\n"
                .format(
                    fraseTexto=self.__frases[frase.id-1],
                    tipoFrase=frase.obterTipoFrase()[TIPO_FRASE],
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
        #a= [ x for x in range(10) ]

        simpleJson = {}
        simpleJson["1.fraseOriginal"] = self.__frases[frase.id-1]
        simpleJson["2.tipo"] = frase.obterTipoFrase()[TIPO_FRASE]
        simpleJson["3.palavrasRelevantes"] = [palavra.palavraOriginal for palavra in frase.obterPalavrasRelevantes()]
        simpleJson["4.voz"] = "Ativa" if frase.isVozAtiva() else "Passiva"
        simpleJson["5.locucaoVerbal"] = frase.possuiLocucaoVerbal()[LOCUCAO_VERBAL_VERBOS] if frase.possuiLocucaoVerbal()[LOCUCAO_VERBAL_POSSUI] else False



        save_to_json("frase{}_dados_completo.json".format(frase.id), toJson)
        save_to_json("frase{}_dados_resumido.json".format(frase.id), simpleJson)

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



