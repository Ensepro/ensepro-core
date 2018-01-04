"""
@project ensepro
@since 04/01/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from ensepro.constantes import SinonimosConstantes
from nltk.corpus import wordnet as wn


def get_sinonimos(word: str, _lang: str) -> list:
    """
    Execute a consulta de sinônimos na wordnet.
    :param word:
    :param _lang:
    :return: Lista de string com os sinônimos retornados pela wordnet. A string estará no formato "^.*\.(a|v|n).([0-9][0-9])\..*$"
    """
    sinonimos = set()
    lemmasDaPalavra = wn.lemmas(word, lang=SinonimosConstantes.LEMMAS_LANG)

    for lemma in lemmasDaPalavra:
        synsetNome = lemma.synset().name()
        synsetLemmas = wn.synset(synsetNome).lemmas(_lang)

        for synsetLemma in synsetLemmas:
            synsetLammaName = synsetLemma.name()
            synsetLemmaSynsetName = synsetLemma.synset().name()

            sinonimo = '.'.join([synsetLemmaSynsetName, synsetLammaName])
            sinonimos.add(sinonimo)

    return list(sinonimos)
