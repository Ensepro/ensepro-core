# -*- coding: utf-8 -*-
"""
@project ensepro
@since 25/02/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
from string import Template
from chatterbot import ChatBot
from ensepro import configuracoes
from ensepro.cln.tipo_frases import TipoFrase
from ensepro.constantes import ChaterbotConstantes, LoggerConstantes

logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_CHATTERBOT_HELPER)

chatter_bot = None
# termos_relevantes = Lista de palavras que devem ser consideradas para obtenção do tipo da frase
termos_relevantes = set()
termos_relevantes_agrupados_por_tipo = {}

KEY_WORDS = ["#"]


def get_tipo(frase):
    if not chatter_bot:
        criar_chatterbot()
        iniciar_treinamento()

    logger.info("Obtendo tipo da frase: %s", frase)
    frase_string = __get_termos_relevantes(frase)

    st = chatter_bot.get_response(frase_string)
    tipo = TipoFrase(st)

    logger.debug("Retorno do chatter_bot: [%s]", st)
    logger.info("Tipo obtido: [%s]", tipo)
    return tipo


def criar_chatterbot():
    logger.info("Criando Chatterbot.")

    nome = configuracoes.get_config(ChaterbotConstantes.NOME)
    storage_adapter = configuracoes.get_config(ChaterbotConstantes.STORAGE_ADAPTER)
    logic_adapters = configuracoes.get_config(ChaterbotConstantes.LOGIC_ADAPTERS)
    trainer = configuracoes.get_config(ChaterbotConstantes.TRAINER)

    logger.debug("Configurações carregadas para criação do Chatterbot: "
                 "[name=%s, storage_adapter=%s, logic_adapters=%s, trainer=%s]",
                 nome, storage_adapter, logic_adapters, trainer)

    global chatter_bot
    chatter_bot = ChatBot(
            name=nome,
            storage_adapter=storage_adapter,
            logic_adapters=logic_adapters,
            trainer=trainer
    )

    logger.info("Chatterbot criado.")


def iniciar_treinamento():
    if not chatter_bot:
        raise Exception("Chatterbot deve ser criado antes do treinamento!")

    logger.info("Iniciando treinamento chatterbot")

    treinamento_carregado = configuracoes.get_config(ChaterbotConstantes.TREINAMENTO)
    logger.debug("Treinamento carregado: [%s]", treinamento_carregado)

    dicionario = treinamento_carregado["dicionario"]
    mapeamento = treinamento_carregado["mapeamento"]

    treinamento_normalizado = __normalizar_treinamento(dicionario, mapeamento)
    logger.debug("Treinamento normalizado: [%s]", treinamento_normalizado)

    logger.info("Treinando....")
    chatter_bot.train(treinamento_normalizado)
    # TODO passar True para arquivo de configuração
    chatter_bot.read_only = True  # após treinamento inicial, bloqueia auto-aprendizagem

    logger.info("Treinamento executado")


def __add_termo_para_treinamento(map_termo, tipo, treinamento_normalizado, dicionario):
    termo = Template(map_termo).substitute(dicionario)
    logger.debug("Termo '%s' normalizado: %s", map_termo, termo)

    __add_termo_relevante(tipo, termo)
    termo = __remover_palavras_chaves(termo)
    treinamento_normalizado.append(termo)
    treinamento_normalizado.append(tipo)


def __normalizar_treinamento(dicionario, mapeamento):
    treinamento_normalizado = []
    for tipo in mapeamento:
        for map_termo in mapeamento[tipo]:
            __add_termo_para_treinamento(map_termo, tipo, treinamento_normalizado, dicionario)
    return treinamento_normalizado


def __remover_palavras_chaves(termo):
    for keyword in KEY_WORDS:
        termo = termo.replace(keyword, "")
    return termo


def __add_termo_relevante(tipo: str, termos: str):
    for termo in termos.split(' '):
        if termo[0] == KEY_WORDS[0]:
            __add_termo_relevante_lista(termo[1:])
            __add_termo_relevante_agrupado_por_tipo(tipo, termo[1:])


def __add_termo_relevante_agrupado_por_tipo(tipo, termo):
    global termos_relevantes_agrupados_por_tipo
    if not tipo in termos_relevantes_agrupados_por_tipo:
        termos_relevantes_agrupados_por_tipo[tipo] = []
    termos_relevantes_agrupados_por_tipo[tipo].append(termo)


def __add_termo_relevante_lista(termo: str):
    global termos_relevantes
    termos_relevantes.add(termo)
    logger.debug("Termo relevante adicionado. [termo='%s']", termo)


def __get_termos_relevantes(frase):
    logger.debug("Montando frase em texto com apenas termos relevantes")
    frase_string = ""

    for palavra in frase.palavras:
        if palavra.palavra_canonica in termos_relevantes:
            frase_string = ' '.join([frase_string, palavra.palavra_canonica, ' '.join(palavra.tags), ''])

    logger.debug("String da frase criada: [frase_string='%s']", frase_string)
    return frase_string.strip(' ')
