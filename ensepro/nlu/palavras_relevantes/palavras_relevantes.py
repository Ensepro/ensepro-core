"""
@project ensepro
@since 26/01/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import re
from ensepro import configuracoes
from ensepro.constantes import ConfiguracoesConstantes

regex_palavra_relevante = re.compile(configuracoes.get_config(ConfiguracoesConstantes.REGEX_PALAVRA_RELEVENTE))


def get(frase):
    return frase.get_palavras(__is_palavra_relevante)


def __is_palavra_relevante(palavra):
    # 1. Palavras que possuem palavraOriginal vazia.
    if not palavra.palavra_original:
        return False

    # 2.1. Palavras não deve fazer parte do tipo da frase
    # 2.2. Se a primeira palavra após o tipo for um verbo de ligação, ignora-lá


    # 3. tagInicial da palavra deve bater com a regex de palavras relevantes
    if not regex_palavra_relevante.search(palavra.tag_inicial):
        return False

    # 4. Quando a frase estiver a voz passiva, o verbo 'ser' deve ser ignorado.


    # 5. Quando houver locução verbal, o(s) verbo(s) auxiliar(es) deve ser desconsiderado.
    #    O verbo relevante SEMPRE será o último.
