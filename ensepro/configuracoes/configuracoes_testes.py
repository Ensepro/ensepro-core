"""
@project ensepro
@since 19/12/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from ensepro.configuracoes import configuracoes as conf
from ensepro.constantes import ConfiguracoesConstantes



print(conf.get_config(ConfiguracoesConstantes.SINONIMOS))
print(conf.get_config(ConfiguracoesConstantes.SERVIDORES))
print(conf.get_config(ConfiguracoesConstantes.FRASES))



