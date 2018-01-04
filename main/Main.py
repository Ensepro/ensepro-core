"""
@project ensepro
@since 20/07/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import sys
import configuracoes
from utils.StringUtil import isEmpty
from constantes.StringConstantes import UTF_8
from constantes.StringConstantes import FILE_READ_ONLY
from constantes.StringConstantes import BREAK_LINE
from main.Ensepro import Ensepro

"""
-m "{frase}"  -> frase a ser analisada  
-tree         -> cria um arquivo com a árvore desenhada.
"""

frases = []
params = {}
ensepro = Ensepro()


def loadParams():
    params["frase"] = "-m" in sys.argv
    if (params["frase"]):
        ensepro.addFrase(sys.argv[sys.argv.index("-m") + 1])
    else:
        carregarFrases()

    ensepro.addParam("tree", "-tree" in sys.argv)


def carregarFrases():
    with open(configuracoes.getPathArquivoFrases(), FILE_READ_ONLY, encoding=UTF_8) as frases:
        for frase in frases:
            frase = frase.replace(BREAK_LINE, "")
            if frase.startswith("#") or isEmpty(frase):
                continue

            ensepro.addFrase(frase)


loadParams()

ensepro.executar()
