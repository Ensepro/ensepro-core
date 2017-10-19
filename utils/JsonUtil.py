"""
@project ensepro
@since 18/10/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import json
from constantes.ConfiguracoesConstantes import SAVE_FILES_TO
from constantes.StringConstantes import FILE_WRITE_READ,UTF_8


def save_to_json(fileName, jsonData):

    with open(SAVE_FILES_TO.format(fileName=fileName), FILE_WRITE_READ, encoding=UTF_8) as result_file:
        result_file.write(json.dumps(jsonData, ensure_ascii=False, indent=4, sort_keys=True))