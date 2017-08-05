"""
@project ensepro
@since 04/08/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from bean.Frase import Frase


def processarFrase(frase : Frase):
    fraseTipo = frase.obterTipoFrase()
    palavrasRelevantes = frase.obterPalavrasRelevantes()
    possuiLocucaoVerbal = frase.possuiLocucaoVerbal()
    vozAtiva = frase.isVozAtiva()

    return {
            "tipo_frase": fraseTipo,
            "palavras_relevantes": palavrasRelevantes,
            "locucao_verbal": possuiLocucaoVerbal,
            "voz_ativa": vozAtiva
            }












