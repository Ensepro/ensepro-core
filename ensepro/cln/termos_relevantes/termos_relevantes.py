# -*- coding: utf-8 -*-
"""
@project ensepro
@since 25/02/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import re
from ensepro import configuracoes
from ensepro.constantes import ConfiguracoesConstantes, ChaterbotConstantes
from ensepro.cln.voz.voz import Voz
from ensepro.cln.tipo_frases.chatterbothelper.chatterbothelper import termos_relevantes_agrupados_por_tipo
from ensepro.utils.string_utils import remover_acentos

regex_termo_relevante = re.compile(configuracoes.get_config(ConfiguracoesConstantes.REGEX_TERMO_RELEVANTE))
verbos_ligacao = configuracoes.get_config(ConfiguracoesConstantes.VERBOS_DE_LIGACAO)
palavras_dos_tipos = {}


def get(frase):
    if __possui_tipo(frase):
        palavras = frase.get_palavras(__possui_palavra_original)
        palavra_tipo = __obtem_palavra_tipo(frase, palavras)
        if palavra_tipo:
            palavra_apos_tipo = __obtem_palavra_apos_tipo(palavras, palavra_tipo)
            return frase.get_palavras(__is_termo_relevante, tipo=palavra_tipo, palavra_apos_tipo=palavra_apos_tipo)

    # Default ignora o tipo para busca de palavras relevantes
    return frase.get_palavras(__is_termo_relevante)


def __is_termo_relevante(frase, palavra, *args):
    # 1. Palavras que possuem palavraOriginal vazia.
    if not palavra.palavra_original:
        return False

    # 2. Se possuir tipo
    if args[0]:
        tipo_id = args[0]["tipo"].id
        palavra_apos_tipo_id = args[0]["palavra_apos_tipo"].id

        # 2.1. Palavras não deve fazer parte do tipo da frase
        if tipo_id >= palavra.id:
            return False

        # 2.2. Se a primeira palavra após o tipo for um verbo de ligação, ignora-lá
        if palavra_apos_tipo_id == palavra.id and palavra.palavra_canonica in verbos_ligacao:
            return False

    # 3. tagInicial da palavra deve bater com a regex de palavras relevantes
    if not regex_termo_relevante.search(palavra.tag_inicial):
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


def __obtem_palavra_tipo(frase, palavras):
    """
    Este método irá determinar qual a palavra que definiu o tipo.
    :param frase: frase sendo analisada
    :return: objeto do tipo Palavra que é a palavra que determinou o tipo
    """
    try:
        termos_relevantes_tipo = termos_relevantes_agrupados_por_tipo[frase.tipo.tipo]
        termos_relevantes_tipo = [remover_acentos(termo) for termo in termos_relevantes_tipo]
        for palavra in palavras:
            if __is_palavra_tipo(palavra, termos_relevantes_tipo):
                return palavra
    except Exception:
        return None

    return None


def __obtem_palavra_apos_tipo(palavras, palavra_tipo):
    index = palavras.index(palavra_tipo)
    return palavras[index + 1]


def __is_palavra_tipo(palavra, termos_do_tipo):
    return remover_acentos(palavra.palavra_canonica) in termos_do_tipo


def __possui_tipo(frase):
    return frase.tipo and frase.tipo.tipo != ChaterbotConstantes.TIPO_DESCONHECIDO


def __possui_palavra_original(frase, palavra, *args):
    return bool(palavra.palavra_original)
