"""
@project ensepro
@since 20/07/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import json
from constantes.StringConstantes import UTF_8
from constantes.StringConstantes import FILE_READ_ONLY
from constantes.ConfiguracoesConstantes import *

def _carregarConfiguracoes():
    """
    Carrega as configurações do arquivo ARQUIVO_CONFIGURACAO (deve estar no formato json)
    :return:
    """
    return json.loads(open(ARQUIVO_CONFIGURACAO, FILE_READ_ONLY, encoding=UTF_8).read())

def getValue(path):
    value = _configuracoes
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

def getUrlService(nomeServicor, nomeServico):
    return getServidorEndpoint(nomeServicor) + getServico(nomeServicor, nomeServico)

# ----------------------------------------------------------------------------------------------------------------------- #
debug = False

try:

    if debug:
        print(MENSAGEM_CARREGANDO.format(fromFile=ARQUIVO_CONFIGURACAO))

    _configuracoes = _carregarConfiguracoes()

    if debug:
        print(MENSAGEM_CARREGAMENTO_SUCESSO)

except Exception as e:
    print(MENSAGEM_CARREGAMENTO_ERRO)
    if debug:
        print(e)
    raise e