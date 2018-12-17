# -*- coding: utf-8 -*-
"""
@project ensepro
@since 25/02/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import re
from ensepro import configuracoes
from ensepro.constantes import ConfiguracoesConstantes, LoggerConstantes

logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_TERMOS_RELEVANTES)
regex_termo_relevante = re.compile(configuracoes.get_config(ConfiguracoesConstantes.REGEX_TERMO_RELEVANTE))
verbos_ligacao = configuracoes.get_config(ConfiguracoesConstantes.VERBOS_DE_LIGACAO)
termos_ignorar = configuracoes.get_config(ConfiguracoesConstantes.TERMOS_RELEVANTES_IGNORAR)


def __is_termo_relevante_base(frase, palavra, *args):
    # 1. Deve ter palavra_canonica
    if not palavra.palavra_canonica:
        logger.debug("'__is_termo_relevante_base' -> palavra '%s' sem palavra canônica", palavra.id)
        return False

    # 2. tagInicial da palavra deve bater com a regex de termos relevantes
    if not regex_termo_relevante.search(palavra.tag_inicial):
        logger.debug("'__is_termo_relevante_base' -> '%s|%s' não está de acordo com a regex de termos relevantes", palavra.id,
                     palavra.palavra_canonica)
        return False

    # # 3. Quando palavra for um ADJ
    # # 3.1. Deve possuir a tag <n> e não deve possuir a tag <NUM-ord>
    # if palavra.is_adjetivo():
    #     if "<n>" not in palavra.tags:
    #         return False
    #     if "<NUM-ord>" in palavra.tags:
    #         return False

    # 4. Não deve ser um verbo de ligação
    if palavra.palavra_canonica in verbos_ligacao:
        logger.debug("'__is_termo_relevante_base' -> palavra '%s|%s' é um verbo de ligação", palavra.id, palavra.palavra_canonica)
        return False

    # 5. Não deve estar na lista de termos a serem ignorados
    if palavra.palavra_canonica in termos_ignorar:
        logger.debug("'__is_termo_relevante_base' -> palavra '%s|%s' é um termo que deve ser ignorado", palavra.id, palavra.palavra_canonica)
        return False

    # 6. Quando houver locução verbal, o(s) verbo(s) auxiliar(es) deve ser desconsiderado.
    #    O verbo relevante SEMPRE será o último.
    if frase.locucao_verbal:
        for locucao_verbal in frase.locucao_verbal:
            if palavra in locucao_verbal[:-1]:
                logger.debug("'__is_termo_relevante_base' -> palavra '%s|%s' parte de uma locução verbal e não é relevante", palavra.id,
                             palavra.palavra_canonica)
                return False

    logger.debug("'__is_termo_relevante_base' -> palavra '%s|%s' é relevante", palavra.id, palavra.palavra_canonica)
    return True


def __is_termo_relevante_default(frase, palavra, *args):
    # 1. validar base.
    if not __is_termo_relevante_base(frase, palavra, args):
        return False

    # 2. Deve estar após o tipo
    if frase.tipo.ids and palavra.id <= frase.tipo.ids[-1]:
        logger.debug("__is_termo_relevante_default -> palavra '%s|%s' esta antes do tipo da frase", palavra.id, palavra.palavra_canonica)
        return False

    logger.debug("'__is_termo_relevante_default' -> palavra '%s|%s' é relevante ", palavra.id, palavra.palavra_canonica)
    return True


def __is_termo_relevante_eh_um(frase, palavra, *args):
    # 1. validar base.
    if not __is_termo_relevante_base(frase, palavra, args):
        return False

    # 2. Não deve fazer parte do tipo
    if frase.tipo.ids and palavra.id in frase.tipo.ids:
        logger.debug("'__is_termo_relevante_eh_um' -> palavra '%s|%s' faz parte do tipo da frase", palavra.id, palavra.palavra_canonica)
        return False

    logger.debug("'__is_termo_relevante_eh_um' -> palavra '%s|%s' é relevante", palavra.id, palavra.palavra_canonica)
    return True


algoritmo_por_tipo = {
    "eh_um": __is_termo_relevante_eh_um
}


def get(frase):
    logger.info("Obtendo termos relevantes")

    algoritmo = algoritmo_por_tipo.get(frase.tipo.tipo, __is_termo_relevante_default)
    logger.debug("Usando algoritmo '%s'", algoritmo.__name__)

    termos = frase.get_palavras(algoritmo)
    logger.debug("Termos relevantes: %s", termos)

    return termos
