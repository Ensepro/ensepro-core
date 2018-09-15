# -*- coding: utf-8 -*-
"""
@project ensepro
@since 02/07/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
from ensepro import Frase
from ensepro.cbc.fields import Field
from ensepro.cbc.sub_proprio import atualizar_frase
from ensepro.configuracoes import get_config
from ensepro.constantes import ConsultaConstantes
from ensepro.consulta.v2 import query_generator
from ensepro.utils.string_utils import remover_acentos
from ensepro.constantes import LoggerConstantes

peso_subsatntivo_proprio = get_config(ConsultaConstantes.PESO_SUBSANTIVO_PROPRIO)
peso_substantivo_comum = get_config(ConsultaConstantes.PESO_SUBSANTIVO_COMUM)
peso_substantivo_comum_sinonimo = get_config(ConsultaConstantes.PESO_SUBSANTIVO_COMUM_SINONIMO)

peso_verbo = get_config(ConsultaConstantes.PESO_VERBO)
peso_verbo_sinonimo = get_config(ConsultaConstantes.PESO_VERBO_SINONIMO)
peso_verbo_nomilizado = get_config(ConsultaConstantes.PESO_VERBO_NOMILIZADO)
peso_verbo_nomilizado_sinonimo = get_config(ConsultaConstantes.PESO_VERBO_NOMILIZADO_SINONIMO)


logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_CBC)


def __nominalizar_verbos(frase: Frase):
    pass


def __sub_proprio_from_frase(frase: Frase):
    logger.debug("Obtendo substantivos próprios da frase.")
    lista_subsantivos_proprios = []
    substantivos_proprios = [palavra for palavra in frase.termos_relevantes if palavra.is_substantivo_proprio()]

    for substantivo in substantivos_proprios:
        lista_subsantivos_proprios.append(remover_acentos(substantivo.palavra_canonica).lower())
        lista_subsantivos_proprios.append(peso_subsatntivo_proprio)

    logger.debug("Substantivos próprios(+sinonimos) da frase: %s", lista_subsantivos_proprios)
    return lista_subsantivos_proprios


def __sub_comum_from_frase(frase: Frase):
    logger.debug("Obtendo substantivos comuns da frase.")
    lista_subsantivos_comuns = []
    substantivos_comuns = [palavra for palavra in frase.termos_relevantes if palavra.is_substantivo()]

    for substantivo in substantivos_comuns:
        lista_subsantivos_comuns.append(remover_acentos(substantivo.palavra_canonica).lower())
        lista_subsantivos_comuns.append(peso_substantivo_comum)
        lang_group_sinonimos = substantivo.sinonimos

        for lang, sinonimos in lang_group_sinonimos.items():
            for sinonimo in sinonimos:
                lista_subsantivos_comuns.append(remover_acentos(sinonimo.sinonimo).lower())
                lista_subsantivos_comuns.append(peso_substantivo_comum_sinonimo)

    logger.debug("Substantivos comuns (+sinonimos) da frase: %s", lista_subsantivos_comuns)
    return lista_subsantivos_comuns


def __verbos_from_frase(frase: Frase):
    logger.debug("Obtendo verbos da frase.")
    lista_verbos = []
    verbos = [palavra for palavra in frase.termos_relevantes if palavra.is_verbo()]

    for verbo in verbos:
        lista_verbos.append(remover_acentos(verbo.palavra_canonica).lower())
        lista_verbos.append(peso_verbo)

        lang_group_sinonimos = verbo.sinonimos

        for lang, sinonimos in lang_group_sinonimos.items():
            for sinonimo in sinonimos:
                lista_verbos.append(remover_acentos(sinonimo.sinonimo).lower())
                lista_verbos.append(peso_substantivo_comum_sinonimo)

                ##Obter verbos nomolizados e seus sinonimos

    logger.debug("Verbos(+sinonimos) da frase: %s", lista_verbos)
    return lista_verbos


def consultar(frase: Frase):
    logger.info("Executando consulta e montagem das queries da frase")
    frase_atualizada = atualizar_frase(frase)
    if not frase_atualizada:
        return None

    substantivos_proprios = __sub_proprio_from_frase(frase_atualizada)
    substantivos_comuns = __sub_comum_from_frase(frase_atualizada)
    verbos = __verbos_from_frase(frase_atualizada)

    params = {}
    params["termos"] = {}
    params["termos"]["substantivos_proprios"] = substantivos_proprios
    params["termos"]["substantivos_comuns"] = substantivos_comuns
    params["termos"]["verbos"] = verbos
    params["frase"] = frase_atualizada

    resultado_final = query_generator.execute_integration(params)

    return resultado_final