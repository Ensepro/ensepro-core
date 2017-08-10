"""
@project ensepro
@since 03/08/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import requests
import configuracoes

nomeServidor = "palavras"
nomeServico = "analisar_frase"

def analisarFrase(frase : str):
    response = requests.get(
                    configuracoes.getUrlService(nomeServidor, nomeServico).format(frase)
                )
    return response


