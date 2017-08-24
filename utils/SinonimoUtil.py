"""
@project ensepro
@since 23/08/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from bean.Sinonimo import Sinonimo


def stringToSinonimo(sinonimoString, sinonimoNumero):
    sinonimoTemp = sinonimoString.split(".")
    sinonimo = {}
    sinonimo["numero"] = sinonimoNumero
    sinonimo["classeGramatical"] = sinonimoTemp[0]
    sinonimo["distanciaSemantica"] = sinonimoTemp[1]
    sinonimo["sinonimo"] = sinonimoTemp[2]

    return Sinonimo(sinonimo)
