"""
@project ensepro
@since 02/08/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from nltk.corpus import wordnet as wn
from utils import StringUtil

def getSinonimos(word, _lang):
    if(StringUtil.isEmpty(word) or StringUtil.isEmpty(_lang)):
        return list()

    sinonimos = set()
    lemmasDaPalavra = wn.lemmas(word, lang=_lang)
    for lemma in lemmasDaPalavra:
        synsetNome = lemma.synset().name()
        synsetLemmas = wn.synset(synsetNome).lemmas(_lang)
        for synsetLemma in synsetLemmas:
            synsetLemmaName = synsetLemma.synset().name()
            sinonimo = synsetLemmaName[synsetLemmaName.index(".") + 1:] + "." + synsetLemma.name()
            sinonimos.add(sinonimo)

    return list(sinonimos)