"""
@project ensepro
@since 21/01/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
from ensepro.constantes import LoggerConstantes

logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_LOCUCAO_VERBAL)


def get(frase):
    logger.info("Buscando locuções verbais: [%s]", frase)

    palavras = frase.get_palavras(__condicao_palavra_original_nao_vazia)
    logger.debug("Palavras com palavra original não vazia: [%s]", palavras)

    numero_palavras = len(palavras)
    locucoes = []
    map_locucao_atual = {}
    palavra_anterior = None

    for index in range(numero_palavras):
        palavra_atual = palavras[index]

        # Se a palavra anterior e a palavra atual forem verbos, existe um locução verbal
        if palavra_anterior and palavra_anterior.is_verbo() and palavra_atual.is_verbo():
            map_locucao_atual[palavra_anterior.id] = palavra_anterior
            map_locucao_atual[palavra_atual.id] = palavra_atual
            logger.debug("Locução encontrada: [palavra_atual=%s, palavra_anterior=%s]", palavra_atual, palavra_anterior)
        else:
            # Caso já tenha encontrado um locução verbal, irá adicionar a lista de locuções
            if map_locucao_atual:
                locucoes.append(__locucao_to_list(map_locucao_atual))
                logger.debug("Adicionando locução verbal a lista de locuções: [locucoes=%s]", locucoes)

                map_locucao_atual = {}

            palavra_anterior = palavra_atual

        index += 1

    # Caso a última palavra seja um verbo, está última locução não terá sido adicionada a lista de locuções
    if map_locucao_atual:
        locucoes.append(__locucao_to_list(map_locucao_atual))
        logger.debug("Adicionando locução verbal a lista de locuções: [locucoes=%s]", locucoes)

    logger.info("Locuções encontradas: [locucoes=%s]", locucoes)
    return locucoes


def __locucao_to_list(locucoes_map):
    return [locucoes_map[id] for id in locucoes_map]


def __condicao_palavra_original_nao_vazia(frase, palavra, *args) -> bool:
    if palavra.palavra_original and palavra.palavra_original.strip():
        return True
    return False
