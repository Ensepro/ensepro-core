"""
@project ensepro
@since 26/01/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import re
from ensepro import configuracoes
from ensepro.constantes import ConfiguracoesConstantes
from ensepro.nlu.voz.voz import Voz
from ensepro.utils.string_utils import remover_acentos

regex_palavra_relevante = re.compile(configuracoes.get_config(ConfiguracoesConstantes.REGEX_PALAVRA_RELEVENTE))


def get(frase):
    palavras_tipo = None
    if frase.tipo.tipo != "desconhecida":
        palavras_tipo = [palavra for palavra in frase.palavras if remover_acentos(palavra.palavra_canonica) == remover_acentos(frase.tipo.tipo)]


    return frase.get_palavras(__is_palavra_relevante, palavras_tipo)


def __is_palavra_relevante(frase, palavra, *args):
    # 1. Palavras que possuem palavraOriginal vazia.
    if not palavra.palavra_original:
        return False

    # 2.1. Palavras não deve fazer parte do tipo da frase
    print(args[0])
    print(args)
    if args and args[0]:
        if args[0].id >= palavra.id:
            return False

    # 2.2. Se a primeira palavra após o tipo for um verbo de ligação, ignora-lá

    # 3. tagInicial da palavra deve bater com a regex de palavras relevantes
    if not regex_palavra_relevante.search(palavra.tag_inicial):
        return False

    # 4. Quando a frase estiver a voz passiva, o verbo 'ser' deve ser ignorado.
    if frase.voz == Voz.PASSIVA and palavra.palavra_canonica == "ser":
        return False

    # 5. Quando houver locução verbal, o(s) verbo(s) auxiliar(es) deve ser desconsiderado.
    #    O verbo relevante SEMPRE será o último.

    return True
