"""
@project ensepro
@since 26/01/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import re
from ensepro import configuracoes
from ensepro.constantes import ConfiguracoesConstantes, ChaterbotConstantes
from ensepro.nlu.voz.voz import Voz
from ensepro.utils.string_utils import remover_acentos

regex_palavra_relevante = re.compile(configuracoes.get_config(ConfiguracoesConstantes.REGEX_PALAVRA_RELEVENTE))
verbos_ligacao = configuracoes.get_config(ConfiguracoesConstantes.VERBOS_DE_LIGACAO)


def get(frase):
    if frase.tipo.tipo != ChaterbotConstantes.TIPO_DESCONHECIDO:
        palavras_tipo = frase.get_palavras(__is_tipo)
        if palavras_tipo:
            return frase.get_palavras(__is_palavra_relevante, tipo=palavras_tipo[0])

    # Default ignora o tipo para busca de palavras relevantes
    return frase.get_palavras(__is_palavra_relevante)


def __is_tipo(frase, palavra, *args):
    return remover_acentos(palavra.palavra_canonica) == remover_acentos(frase.tipo.tipo)


def __is_palavra_relevante(frase, palavra, *args):
    # 1. Palavras que possuem palavraOriginal vazia.
    if not palavra.palavra_original:
        return False

    # 2. Se possuir tipo
    if args[0]:
        tipo_id = args[0]["tipo"].id
        palavra_anterior_era_tipo = False
        # 2.1. Palavras não deve fazer parte do tipo da frase
        if tipo_id >= palavra.id:
            palavra_anterior_era_tipo = tipo_id == palavra.id
            return False
        # 2.2. Se a primeira palavra após o tipo for um verbo de ligação, ignora-lá
        if palavra_anterior_era_tipo and palavra.palavra_canonica in verbos_ligacao:
            return False

    # 3. tagInicial da palavra deve bater com a regex de palavras relevantes
    if not regex_palavra_relevante.search(palavra.tag_inicial):
        return False

    # 4. Quando a frase estiver a voz passiva, o verbo 'ser' deve ser ignorado.
    if frase.voz == Voz.PASSIVA and palavra.palavra_canonica == "ser":
        return False

    # 5. Quando houver locução verbal, o(s) verbo(s) auxiliar(es) deve ser desconsiderado.
    #    O verbo relevante SEMPRE será o último.
    if frase.locucao_verbal:
        for locucao_verbal in frase.locucao_verbal:
            if palavra in locucao_verbal[:-1]:
                return False

    return True
