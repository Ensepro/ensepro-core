"""
@project ensepro
@since 04/01/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import json
from ensepro.constantes import ConfiguracoesConstantes, StringConstantes


def __carregar_configuracoes():
    global __configs
    __configs = json.loads(open(
            file=ConfiguracoesConstantes.ARQUIVO_CONFIGURACOES,
            mode=StringConstantes.FILE_READ_ONLY,
            encoding=StringConstantes.UTF_8
    ).read())


def __get_config(path):
    value = __configs
    _path = path.split(".")
    for key in _path:
        value = value[key]
    return value


def get_config(path: str, path_params=None, config_params=None) -> str:
    """
    Obtém a configuração (<i>path</i>) do arquivo de configuração.
    :param path: caminho da configuração no arquivo json, separada por ponto('.').
    :param path_params: mapa com os parametros necessários para preencher o caminho da configuração.
    :param config_params: mapa com os parametros necessários para completar a configuração obtida
    :return:
    """
    # TODO: #ADD_LOG
    if path_params:
        path = path.format_map(path_params)

    config = __get_config(path)

    if config_params:
        return config.format_map(config_params)

    return config


__carregar_configuracoes()
