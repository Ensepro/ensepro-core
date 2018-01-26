"""
@project ensepro
@since 26/01/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""


def get(frase):
    return frase.get_palavras(__is_palavra_relevante)


def __is_palavra_relevante(palavra):
    # 1. Palavras que possuem palavraOriginal vazia.
    if not palavra.palavra_original:
        return False
    # 2. Palavras não deve fazer parte do tipo da frase
    # 3. tagInicial da palavra deve bater com a regex de palavras relevantes
    # 4. Quando a frase estiver a voz passiva, o verbo 'ser' deve ser ignorado.
    # 5. Quando houver locução verbal, o(s) verbo(s) auxiliar(es) deve ser desconsiderado.
    #    O verbo relevante SEMPRE será o último.
