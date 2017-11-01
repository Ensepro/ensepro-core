"""
@project ensepro
@since 04/08/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from bean.Frase import Frase
from constantes.NLUConstantes import *


def processarFrase(frase: Frase):
    fraseTipo = frase.obterTipoFrase()
    possuiLocucaoVerbal = frase.possuiLocucaoVerbal()
    vozAtiva = frase.isVozAtiva()
    palavrasRelevantes = frase.obterPalavrasRelevantes()
    adjuntosComplementos = frase.getAdjuntosComplementos()

    return {
        TIPO_FRASE: fraseTipo,
        PALAVRAS_RELEVANTES: palavrasRelevantes,
        LOCUCAO_VERBAL: possuiLocucaoVerbal,
        VOZ_ATIVA: vozAtiva,
        NOME_COMPLEMENTO: adjuntosComplementos
    }
