"""
@project ensepro
@since 17/10/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import configuracoes

ERROR = configuracoes.getLog() == "error"
DEBUG = ERROR or configuracoes.getLog() == "debug"
INFO = ERROR or DEBUG or configuracoes.getLog() == "info"

