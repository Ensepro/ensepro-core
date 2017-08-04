"""
@project ensepro
@since 20/07/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import requests

import configuracoes
import tipofrases
from servicos import Palavras as palavras
from bean.Frase import Frase
from bean.Palavra import Palavra

print("Virtuoso endpoint: "+configuracoes.getServidorEndpoint("virtuoso"))
print("Serviços: "+str(configuracoes.getServicos("virtuoso")))
print("Palavras endpoint"+configuracoes.getServidorEndpoint("palavras"))
print("Serviços: "+str(configuracoes.getServicos("palavras")))
print("Serviços: "+str(configuracoes.getServico("palavras", "analisar_frase")))

fraseTexto = "quais doutorandos estão trabalhando na CWI?"
fraseAnalisada = palavras.analisarFrase(fraseTexto)

print(fraseAnalisada.content)


