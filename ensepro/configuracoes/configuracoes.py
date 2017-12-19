"""
@project ensepro
@since 18/12/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import json
from ensepro.commons.commons import FILE_READ_ONLY, UTF_8

ARQUIVO_CONFIGURACOES = "./configs.json"


def __carregar_configuracoes():
    global __configs
    __configs = json.loads(open(ARQUIVO_CONFIGURACOES, FILE_READ_ONLY, encoding=UTF_8).read())


def get_config(path):
    value = __configs
    _path = path.split(".")
    for key in _path:
        value = value[key]
    return value
