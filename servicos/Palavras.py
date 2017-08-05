"""
@project ensepro
@since 03/08/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import requests
import configuracoes

nome_servidor = "palavras"

def analisarFrase(frase : str):
    response = requests.get(
                    _buildUrlService("analisar_frase").replace("{frase}", frase)
                )
    return response

def _buildUrlService(nomeServico):
    return configuracoes.getServidorEndpoint(nome_servidor) + configuracoes.getServico(nome_servidor, nomeServico)
