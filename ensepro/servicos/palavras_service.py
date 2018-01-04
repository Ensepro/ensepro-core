"""
@project ensepro
@since 04/01/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import requests
import ensepro.configuracoes as configuracoes
from ensepro.constantes import PalavrasServidorConstantes as ps_consts


def analisar_frase(frase: str):
    # TODO: #ADD_LOG
    response = requests.get(
            configuracoes.get_config(ps_consts.SERVICO_ANALISAR_FRASE, config_params={ps_consts.ANALISAR_FRASE_PARAM: frase})
    )
    return response
