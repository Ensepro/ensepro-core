# -*- coding: utf-8 -*-
"""
@project ensepro
@since 25/02/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
from ensepro.cln.complementos_nominais import ComplementoNominal
from ensepro.constantes import LoggerConstantes

logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_COMPLEMENTOS_NOMINAIS)


def get(frase):
    logger.info("Obtendo complementos nominais para frase: [%s]", frase)
    complementos_nominais = []
    for palavra in frase.palavras:
        if palavra.tag_inicial in LOGICAS:
            logger.debug("Chamando função '%s' para tag_inicial=%s", LOGICAS[palavra.tag_inicial].__name__, palavra.tag_inicial)
            complemento_nominal = LOGICAS[palavra.tag_inicial](frase, palavra)
            if complemento_nominal and complemento_nominal.ok:
                logger.info("Complemento nominal encontrado: [%s]", complemento_nominal)
                complementos_nominais.append(complemento_nominal)

    return complementos_nominais


def __dn_adj(frase, palavra):
    # 1. Obter o nucleo do node pai do node da palavra
    nome = __obtem_nucleo_node_pai(frase, palavra, NUCLEOS[palavra.tag_inicial])
    # 2. A própria palavra é o complemento
    complemento = palavra

    return ComplementoNominal(nome, complemento)


def __dn_prop(frase, palavra):
    return __dn_adj(frase, palavra)


def __dn_num(frase, palavra):
    return __dn_adj(frase, palavra)


def __dn_adjp(frase, palavra):
    return __dn_np(frase, palavra)


def __dn_v_pcp(frase, palavra):
    return __dn_adj(frase, palavra)


def __dn_np(frase, palavra):
    # 1. Obter o nucleo do node pai do node da palavra
    nome = __obtem_nucleo_node_pai(frase, palavra, NUCLEOS[palavra.tag_inicial])

    # 2. Obter nucleo do node da palavra
    complemento = __obtem_nucleo_somente_filhos(frase.arvore.nodes[palavra.id], NUCLEOS[palavra.tag_inicial])

    return ComplementoNominal(nome, complemento)


def __dn_pp(frase, palavra):
    # 1. Obter o nucleo do node pai do node da palavra
    nome = __obtem_nucleo_node_pai(frase, palavra, NUCLEOS[palavra.tag_inicial])

    # 2. Obter o primeiro nucleo abaixo do node da palavra, de forma recursiva
    complemento = __obtem_primeiro_nucleo_abaixo(frase.arvore.nodes[palavra.id], NUCLEOS[palavra.tag_inicial],
                                                 TAG_PARAR_BUSCA_COMPLEMENTOS_NOMINAIS[palavra.tag_inicial])

    return ComplementoNominal(nome, complemento)


NUCLEOS = {
    "DN:prop": ["H:n", "H:adj", "H:prop", "DP:n"],
    "DN:adj": ["H:n", "H:adj", "H:prop", "DP:n"],
    "DN:adjp": ["H:n", "H:adj", "H:prop", "DP:n"],
    "DN:num": ["H:n", "H:adj", "H:prop", "DP:n"],
    "DN:np": ["H:n", "H:adj", "H:prop", "DP:n"],
    "DN:pp": ["H:n", "H:adj", "H:prop", "DP:prop", "DP:n"],
    "DN:v-pcp": ["H:n"],
}

# TODO verificar as tags que devem ir aqui...
TAG_PARAR_BUSCA_COMPLEMENTOS_NOMINAIS = {
    "DN:prop": [],
    "DN:adj": [],
    "DN:adjp": [],
    "DN:num": [],
    "DN:np": [],
    "DN:pp": ["DP:icl"],
    "DN:v-pcp": [],
}

LOGICAS = {
    "DN:prop": __dn_prop,
    "DN:adj": __dn_adj,
    "DN:adjp": __dn_adjp,
    "DN:num": __dn_num,
    "DN:np": __dn_np,
    "DN:pp": __dn_pp,
    "DN:v-pcp": __dn_v_pcp
}


def __obtem_nucleo_node_pai(frase, palavra, nucleos):
    logger.debug("Obtendo nucleo do node pai: [%s]", palavra)
    # 1. Obter node da palavra
    node_palavra = frase.arvore.nodes[palavra.id]
    # 2. Obter node pai da palavra
    node_pai_palavra = node_palavra.pai
    # 3. Obter nucleo do node pai
    nucleo_node_pai = __obtem_nucleo_somente_filhos(node_pai_palavra, nucleos)
    logger.debug("Nucleo do node pai obtido: [%s]", nucleo_node_pai)
    return nucleo_node_pai


def __obtem_nucleo_somente_filhos(node_pai, nucleos: list):
    logger.debug("Buscando nucleo dos filhos: [node_pai='%s']", node_pai)
    for node_filho in node_pai.filhos:
        if node_filho.valor.tag_inicial in nucleos:
            logger.debug("Nucleo encontrado: [nucleo='%s']", node_filho.valor)
            return node_filho.valor

    return None


def __obtem_primeiro_nucleo_abaixo(node, nucleos: list, tags_parar_busca: list):
    """
    Este método vai ir descendo na árvore a partir do 'node' indicado e irá retornar
    o primeiro Nucleo que encontrar. Caso não existe um Nucleo, será retornado None.
    :param node: Node de inicio para a busca do primeiro Nucleo.
    :param nucleos: Lista de Nucleos que serão considerados
    :return:
    """
    if not node:
        return None

    nucleo = __obtem_nucleo_somente_filhos(node, nucleos)

    if nucleo:
        return nucleo

    for node_filho in node.filhos:
        if node_filho.is_nao_terminal and node_filho.valor.tag_inicial not in tags_parar_busca:
            nucleo = __obtem_primeiro_nucleo_abaixo(node_filho, nucleos, tags_parar_busca)
            if nucleo:
                return nucleo

    return None
