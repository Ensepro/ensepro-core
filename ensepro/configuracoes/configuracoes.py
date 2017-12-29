"""
@project ensepro
@since 18/12/2017
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


def get_config(path, params=None):
    if params:
        path.format(params)
    return __get_config(path)


__carregar_configuracoes()
