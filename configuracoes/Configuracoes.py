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

def _validateConfigs():
    """
    Faz a validação se as configurações obrigatórias existem.
    :return:
    """
    _validarConfiguracoesServidores()

def _validarConfiguracoesServidores():
    """
    Faz a validação das configurações dos servidores.
    :return:
    """
    if len(configuracoes[CONFIG_SERVIDORES]) > 0:
        _validarServidor(CONFIG_SERVIDOR_VIRTUOSO)
        _validarServidor(CONFIG_SERVIDOR_PALAVRAS)
    else:
        raise KeyError(CONFIG_SERVIDORES)


def _validarServidor(servidor):
    """
    Faz a validação das configurações de um servidor
    :return:
    """
    if(len(configuracoes[CONFIG_SERVIDORES][servidor]) > 0):
        _validarEndpint(servidor)
    else:
        raise KeyError(CONFIG_SERVIDORES + "/" + servidor)

def _validarEndpint(servidor):
    """
    Valida a existência do atributo endpoint.
    :param servidor:
    :return:
    """
    if configuracoes[CONFIG_SERVIDORES][servidor][CONFIG_ENDPOINT]:
        pass
    else:
        raise KeyError(CONFIG_SERVIDORES + "/" + servidor + "/" + CONFIG_ENDPOINT)

def _getMensagemErro(mensagem, param):
    return mensagem.replace("?", param)



def getServidorEndpoint(servidor):
    return configuracoes[CONFIG_SERVIDORES][servidor][CONFIG_ENDPOINT]

def getServicos(servidor):
    return configuracoes[CONFIG_SERVIDORES][servidor][CONFIG_SERVICOS]

def getServico(servidor, nomeServico):
    return configuracoes[CONFIG_SERVIDORES][servidor][CONFIG_SERVICOS][nomeServico]

def getTipoFrases():
    return configuracoes[CONFIG_TIPO_FRASES]

def getPathArquivoFrases():
    return configuracoes[CONFIG_ARQUIVO_FRASES]


configFile = "../configuracoes/configuracoes.json"
debug = True

try:
    if debug:
        print(MENSAGEM_CARREGANDO.replace("?", configFile))
    configuracoes = _loadConfigs(configFile)
    _validateConfigs()
    if debug:
        print(MENSAGEM_CARREGAMENTO_SUCESSO)
except KeyError as e:
    print(_getMensagemErro(MENSAGEM_CARREGAMENTO_ERRO, configFile))
    if debug:
        print(_getMensagemErro(MENSAGEM_ERRO, str(e)))
except Exception as e:
    print(MENSAGEM_CARREGAMENTO_ERRO)
    if debug:
        print(e)