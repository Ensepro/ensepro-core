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
    set_locucao_verbal = set()
    palavra_anterior = None

    for index in range(numero_palavras):
        palavra_atual = palavras[index]

        # Se a palavra anterior e a palavra atual forem verbos, existe um locução verbal
        if palavra_anterior and palavra_anterior.is_verbo() and palavra_atual.is_verbo():
            set_locucao_verbal.add(palavra_atual)
            set_locucao_verbal.add(palavra_anterior)
            logger.debug("Locução encontrada: [palavra_atual=%s, palavra_anterior=%s]", palavra_atual, palavra_anterior)
        else:
            # Caso já tenha encontrado um locução verbal, irá adicionar a lista de locuções
            if set_locucao_verbal:
                locucoes.append(list(set_locucao_verbal))
                logger.debug("Adicionando locução verbal a lista de locuções: [locucoes=%s]", locucoes)

                set_locucao_verbal = set()

            palavra_anterior = palavra_atual

        index += 1

    # Caso a última palavra seja um verbo, está última locução não terá sido adicionada a lista de locuções
    if set_locucao_verbal:
        locucoes.append(list(set_locucao_verbal))
        logger.debug("Adicionando locução verbal a lista de locuções: [locucoes=%s]", locucoes)

    logger.info("Locuções encontradas: [locucoes=%s]", locucoes)
    return locucoes


def __condicao_palavra_original_nao_vazia(palavra) -> bool:
    if palavra.palavra_original and palavra.palavra_original.strip():
        return True
    return False
