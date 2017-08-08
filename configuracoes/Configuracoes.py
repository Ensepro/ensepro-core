"""
@project ensepro
@since 20/07/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import json
from constantes.StringConstantes import UTF_8
from constantes.ConfiguracoesConstantes import *

def _loadConfigs(fromFile):
    """
    Carrega as configurações do arquivo 'fromFile' (deve estar no formato json)
    :param fromFile:
    :return:
    """
    return json.loads(open(fromFile, 'r', encoding=UTF_8).read())

def getValue(path):
    value = configuracoes
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
    return getValue(CONFIG_ARQUIVO_FRASES)

def getSparqlQueries():
    return getValue(CONFIG_QUERIES_SPARQL.format(nome_servidor=SERVIDOR_VIRTUOSO))



configFile = "../configuracoes/configuracoes.json"
debug = True

try:

    if debug:
        print(MENSAGEM_CARREGANDO.format(fromFile=configFile))

    configuracoes = _loadConfigs(configFile)

    if debug:
        print(MENSAGEM_CARREGAMENTO_SUCESSO)

except Exception as e:
    print(MENSAGEM_CARREGAMENTO_ERRO)
    if debug:
        print(e)