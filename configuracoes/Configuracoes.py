"""
@project ensepro
@since 20/07/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import json
from constantes.StringConstantes import UTF_8
from constantes.StringConstantes import FILE_READ_ONLY
from constantes.ConfiguracoesConstantes import *


def __carregarConfiguracoes():
    """
    Carrega as configurações do arquivo ARQUIVO_CONFIGURACAO (deve estar no formato json)
    :return:
    """
    return json.loads(open(ARQUIVO_CONFIGURACAO, FILE_READ_ONLY, encoding=UTF_8).read())


def init():
    global __configuracoes

    try:
        __configuracoes = __carregarConfiguracoes()

    except Exception as e:
        raise e

init()

def getValue(path):
    value = __configuracoes
    _path = path.split("/")
    for key in _path:
        value = value[key]
    return value


def getServidorEndpoint(servidor):
    return getValue(CONFIG_ENDPOINT.format(nome_servidor=servidor))

def getServicos(servidor):
    return getValue(CONFIG_SERVICOS.format(nome_servidor=servidor))

def getServico(servidor, nomeServico):
    return getValue(CONFIG_SERVICO.format(nome_servidor=servidor, nome_servico=nomeServico))

def getTipoFrases():
    return getValue(CONFIG_TIPO_FRASES)

def getPathArquivoFrases():
    return ENSEPRO_PATH + getValue(CONFIG_ARQUIVO_FRASES)

def getRegexPalavraRelevante():
    return getValue(CONFIG_REGEX_PALAVRA_RELEVENTE)

def getRegexPalavraVerbo():
    return getValue(CONFIG_REGEX_PALAVRA_VERBO)

def getRegexPalavraAdjetivo():
    return getValue(CONFIG_REGEX_PALAVRA_ADJETIVO)

def getRegexPalavraSubstantivo():
    return getValue(CONFIG_REGEX_PALAVRA_SUBSTANTIVO)

def getRegexPalavraPreposicao():
    return getValue(CONFIG_REGEX_PALAVRA_PREPOSICAO)

def getRegexVozPassiva():
    return getValue(CONFIG_REGEX_VOZ_PASSIVA)

def getSinonimosLinguagens():
    return getValue(CONFIG_SINONIMOS_LINGUAGENS)

def getPortaServidor(nomeServidor):
    return getValue(CONFIG_PORTA.format(nome_servidor=nomeServidor))

def getLog():
    return getValue(CONFIG_LOG)

def getElasticSearchSettings():
    return getValue(CONFIG_SETTINGS.format(nome_servidor=SERVIDOR_ELASTIC_SEARCH))

def getUrlService(nomeServidor, nomeServico):
    return getServidorEndpoint(nomeServidor) +":"+ getPortaServidor(nomeServidor) + getServico(nomeServidor, nomeServico)