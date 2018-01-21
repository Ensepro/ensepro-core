"""
@project ensepro
@since 04/01/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import json
import logging
from ensepro.constantes import ConfiguracoesConstantes, StringConstantes, LoggerConstantes


def __init_logger():
    global logger

    logging.basicConfig(
            filename=__get_config(LoggerConstantes.NOME_DO_ARQUIVO),
            level=logging.INFO,
            format=__get_config(LoggerConstantes.FORMATO)
    )
    logger = logging.getLogger(LoggerConstantes.GET_LOGGER_MODULO.format(modulo=LoggerConstantes.MODULO_CONFIGURACOES))
    logger.setLevel(logging.getLevelName(__get_config(LoggerConstantes.NIVEL_LOG_MODULO.format(modulo=LoggerConstantes.MODULO_CONFIGURACOES))))


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
    logger.debug("Obtendo configuração: [path=%s, path_params=%s, config_params=%s]", path, path_params, config_params)
    if path_params:
        path = path.format_map(path_params)

    config = __get_config(path)

    if config_params:
        return config.format_map(config_params)

    logger.info("Configuração obtida: [path=%s] = %s", path, config)
    return config


__carregar_configuracoes()
__init_logger()
