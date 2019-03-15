# -*- coding: utf-8 -*-
"""
@project ensepro
@since 02/07/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
from ensepro import Frase
from ensepro.cbc.answer_generator import answer_generator
from ensepro.cbc.fields import Field
from ensepro.cbc.sub_proprio import atualizar_frase
from ensepro.cln import nominalizacao
from ensepro.configuracoes import get_config
from ensepro.constantes import ConsultaConstantes
from ensepro.constantes import LoggerConstantes
from ensepro.utils.string_utils import remover_acentos

peso_substantivo_proprio = get_config(ConsultaConstantes.PESO_SUBSANTIVO_PROPRIO)
peso_substantivo_comum = get_config(ConsultaConstantes.PESO_SUBSANTIVO_COMUM)
peso_substantivo_comum_sinonimo = get_config(ConsultaConstantes.PESO_SUBSANTIVO_COMUM_SINONIMO)

peso_verbo = get_config(ConsultaConstantes.PESO_VERBO)
peso_verbo_sinonimo = get_config(ConsultaConstantes.PESO_VERBO_SINONIMO)
peso_verbo_nomilizado = get_config(ConsultaConstantes.PESO_VERBO_NOMILIZADO)
peso_verbo_nomilizado_sinonimo = get_config(ConsultaConstantes.PESO_VERBO_NOMILIZADO_SINONIMO)

peso_adjetivo = get_config(ConsultaConstantes.PESO_ADJETIVO)

logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_CBC)


def __nominalizar_verbos(frase: Frase):
    pass


def __sub_proprio_from_frase(frase: Frase, ignore):
    logger.debug("Obtendo substantivos próprios da frase.")
    lista_subsantivos_proprios = []
    substantivos_proprios = [palavra for palavra in frase.termos_relevantes if palavra.is_substantivo_proprio()]

    for substantivo in substantivos_proprios:
        palavra = remover_acentos(substantivo.palavra_canonica).lower()
        if palavra in ignore:
            continue
        lista_subsantivos_proprios.append(palavra)
        lista_subsantivos_proprios.append(peso_substantivo_proprio)

    logger.debug("Substantivos próprios(+sinonimos) da frase: %s", lista_subsantivos_proprios)
    return lista_subsantivos_proprios


def __sub_comum_from_frase(frase: Frase, ignore):
    logger.debug("Obtendo substantivos comuns da frase.")
    lista_subsantivos_comuns = []
    substantivos_comuns = [
        palavra for palavra in frase.termos_relevantes
        if palavra.is_substantivo()  # or palavra.is_adjetivo()
    ]

    for substantivo in substantivos_comuns:
        palavra = remover_acentos(substantivo.palavra_canonica).lower()
        if palavra == ignore:
            continue
        lista_subsantivos_comuns.append(palavra)
        lista_subsantivos_comuns.append(peso_substantivo_comum)
        lang_group_sinonimos = substantivo.sinonimos

        for lang, sinonimos in lang_group_sinonimos.items():
            for sinonimo in sinonimos:
                if len(sinonimo.sinonimo) > 2:
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

        nominalizacoes_verbo = nominalizacao.get(verbo.palavra_canonica)

        for nom in nominalizacoes_verbo:
            if nom not in lista_verbos:
                lista_verbos.append(remover_acentos(nom).lower())
                lista_verbos.append(peso_verbo_nomilizado)

        for lang, sinonimos in lang_group_sinonimos.items():
            for sinonimo in sinonimos:
                if len(sinonimo.sinonimo) > 2 and sinonimo.sinonimo not in lista_verbos:
                    lista_verbos.append(remover_acentos(sinonimo.sinonimo).lower())
                    lista_verbos.append(peso_substantivo_comum_sinonimo)

                # Obter verbos nominalizados dos sinonimos?

    logger.debug("Verbos(+sinonimos) da frase: %s", lista_verbos)
    return lista_verbos


def __adjetivos_nao_tr(frase: Frase):
    logger.debug("Obtendo adjetivos que não são TR")
    lista_adjs = []

    for palavra in frase.palavras:
        if palavra in frase.termos_relevantes:
            continue

        if palavra.is_adjetivo():
            lista_adjs.append(remover_acentos(palavra.palavra_canonica).lower())
            lista_adjs.append(peso_adjetivo)
            lista_adjs.append(remover_acentos(palavra.palavra_original).lower())
            lista_adjs.append(peso_adjetivo)

    logger.debug("Verbos(+sinonimos) da frase: %s", lista_adjs)
    return lista_adjs


def check_sub_query(frase: Frase):
    logger.info("Verificando necessidade de subquery.")
    cns = frase.complementos_nominais
    trs = frase.termos_relevantes
    size_cn = len(cns)
    size_tr = len(trs)
    if size_tr < 3:
        logger.info("Subquery não necessária. [menos de 3 TRs]")
        return None

    if (size_cn * 2) >= size_tr:
        logger.info("Subquery não necessária. [(size_cn * 2) >= size_tr]")
        return None

    for cn in cns:
        if cn.complemento.is_substantivo_proprio() and not cn.nome.is_substantivo_proprio():
            logger.info("Subquery necessária.")
            sub_query_values = {
                "prop": cn.complemento,
                "verb": cn.nome
            }
            logger.debug("Subquery - valores encontrados - %s - %s", str(cn.nome), str(cn.complemento))
            return sub_query_values

    logger.info("Subquery não necessária.")
    return None


def sub_query_and_update(check_result):
    verb = remover_acentos(check_result["verb"].palavra_canonica).lower()
    prop = remover_acentos(check_result["prop"].palavra_canonica).lower()

    frase = Frase(palavras=[check_result["verb"], check_result["prop"]], frase="subquery of: " + verb + " + " + prop)

    params = {}
    params["termos"] = {}
    params["termos"]["PROP"] = [prop, peso_substantivo_proprio]
    params["termos"]["VERB"] = [verb, peso_substantivo_comum]
    params["frase"] = frase
    params["nao_relacionar"] = True

    import json
    logger.info("Executando subquery: %s", json.dumps(params))

    resultado = answer_generator.execute_integration(params)

    logger.debug("resultado subquery: %s", json.dumps(resultado))
    props = []

    if not resultado:
        return None

    if not resultado["all_answers"]:
        return None

    best_result_score = resultado["all_answers"][0]["score"]

    for result in resultado["all_answers"]:
        if result["score"] == best_result_score:
            triple = result["triples"][0]
            if triple[1][0] == "*":
                if triple[0][0] == "*":
                    props.append(triple[2])
                    props.append(peso_substantivo_proprio)
                    logger.info("Subquery result: %s", triple[2])
                    continue
                if triple[2][0] == "*":
                    props.append(triple[0])
                    props.append(peso_substantivo_proprio)
                    logger.info("Subquery result: %s", triple[0])
                    continue
        logger.info("Subquery não obteve resultados")
        break

    return {
        "resultado": props,
        "substantivos_remover": verb,
        "substantivos_proprios_remover": prop
    }


def consultar(frase: Frase):
    logger.info("Executando consulta e montagem das queries da frase")
    if not frase:
        return None

    check_sub_query_result = check_sub_query(frase)

    sub_query_result = []
    sub_proprio_from_subquery = []
    substantivos_proprios_remover = ""
    substantivos_remover = ""
    if check_sub_query_result:
        sub_query_result = sub_query_and_update(check_sub_query_result)
        if sub_query_result and sub_query_result["resultado"]:
            sub_proprio_from_subquery = sub_query_result["resultado"]
            substantivos_proprios_remover = sub_query_result["substantivos_proprios_remover"]
            substantivos_remover = sub_query_result["substantivos_remover"]

    logger.debug("subquery resultado final: %s", str(sub_query_result))

    substantivos_proprios = __sub_proprio_from_frase(frase, substantivos_proprios_remover)
    substantivos_comuns = __sub_comum_from_frase(frase, substantivos_remover)
    verbos = __verbos_from_frase(frase)
    adjetivos_nao_tr = __adjetivos_nao_tr(frase)

    params = {}
    params["termos"] = {}
    params["termos"]["PROP"] = substantivos_proprios + sub_proprio_from_subquery
    params["termos"]["SUB"] = substantivos_comuns
    params["termos"]["VERB"] = verbos
    params["termos"]["ADJ"] = adjetivos_nao_tr
    params["frase"] = frase

    resultado_final = answer_generator.execute_integration(params)

    return resultado_final
