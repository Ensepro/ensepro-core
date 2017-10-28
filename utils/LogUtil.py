"""
@project ensepro
@since 17/10/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from constantes.LogConstantes import *
from datetime import datetime

def error(mensagem):
    if ERROR:
        print("ERRO:::" + str(datetime.now()) + " -- " + str(mensagem))


def debug(mensagem):
    if DEBUG:
        print("DEBUG::" + str(datetime.now()) + " -- " + str(mensagem))


def info(mensagem):
    if info:
        print("INFO:::" + str(datetime.now()) + " -- " + str(mensagem))
