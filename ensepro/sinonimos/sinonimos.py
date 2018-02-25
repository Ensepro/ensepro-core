# -*- coding: utf-8 -*-
"""
@project ensepro
@since 25/02/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from ensepro.constantes import SinonimosConstantes, LoggerConstantes
from nltk.corpus import wordnet as wn

logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_SINONIMOS)


def get_sinonimos(palavra: str, lang: str) -> list:
    """
    Execute a consulta de sinônimos na wordnet.
    :param palavra: palavra que se deve bucar os sinônimos
    :param lang: linguagem(abreviação) dos quais os sinônimos devem ser tradidos
    :return: Lista de string com os sinônimos retornados pela wordnet. A string estará no formato "^.*\.(a|v|n).([0-9][0-9])\..*$"
    """
    logger.info("Buscando sinonimos: [palavra=%s, lang=%s]", palavra, lang)
    sinonimos = set()

    lemmasDaPalavra = wn.lemmas(palavra, lang=SinonimosConstantes.LEMMAS_LANG)
    logger.debug("Lemmas da palavra '%s' com lang=%s: %s", palavra, SinonimosConstantes.LEMMAS_LANG, lemmasDaPalavra)

    for lemma in lemmasDaPalavra:
        synsetNome = lemma.synset().name()
        synsetLemmas = wn.synset(synsetNome).lemmas(lang)

        for synsetLemma in synsetLemmas:
            synsetLammaName = synsetLemma.name()
            synsetLemmaSynsetName = synsetLemma.synset().name()

            sinonimo = '.'.join([synsetLemmaSynsetName, synsetLammaName])
            sinonimos.add(sinonimo)

            logger.debug("[lemma=%s] = [synsetNome=%s, synsetLemmas=%s] = [synsetLammaName=%s, synsetLemmaSynsetName=%s] = [sinonimo=%s]",
                         lemma, synsetNome, synsetLemmas, synsetLammaName, synsetLemmaSynsetName, sinonimo)

    logger.info("Sinonimos obtidos: %s", str(sinonimos))
    return list(sinonimos)
