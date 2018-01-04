"""
@project ensepro
@since 19/12/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from ensepro.configuracoes import configuracoes as conf
from ensepro.constantes import ConfiguracoesConstantes, PalavrasServidorConstantes

print(conf.get_config(ConfiguracoesConstantes.SINONIMOS))
print(conf.get_config(ConfiguracoesConstantes.SERVIDORES))
print(conf.get_config(ConfiguracoesConstantes.FRASES))

print(conf.get_config(PalavrasServidorConstantes.SERVICO_ANALISAR_FRASE, config_params={"frase": "FRASE-DE-TESTE"}))
