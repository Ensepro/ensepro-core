"""
@project ensepro
@since 04/01/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from ensepro import sinonimos
from ensepro.sinonimos import Sinonimo
from ensepro.classes.palavra import Palavra

sinonimos_retornados = sinonimos.get_sinonimos("andar", "por")
print(sinonimos_retornados, end='\n\n')

print("teste1:  ", end='')

teste1 = sinonimos_retornados[0]
sinonimo = Sinonimo.from_string(teste1)
print(sinonimo)


#########
dados_palavra = {
    "tags": ["tag1", "tag2", "tag3"],
    "nivel": "2",
    "tag_inicial": "DN:adj",
    "palavra_original": "estar",
    "palavra_canonica": "estar"

}
palavra = Palavra(id="TesteSinonimos1", dados_palavra=dados_palavra)

print(palavra.sinonimos)