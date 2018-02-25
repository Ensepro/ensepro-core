# -*- coding: utf-8 -*-
"""
@project ensepro
@since 25/02/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""


def path():
    import os
    return os.path.abspath("../../")


class SinonimosConstantes:
    LEMMAS_LANG = "por"


class StringConstantes:
    UTF_8 = "utf-8"
    BREAK_LINE = "\n"
    TAB = "\t"

    FILE_READ_ONLY = 'r'
    FILE_WRITE_ONLY = 'w'
    FILE_WRITE_READ = 'w+'


class ConfiguracoesConstantes:
    PATH = path()
    ARQUIVO_CONFIGURACOES = PATH + "/ensepro/configuracoes/configs.json"

    # Servidores
    SERVIDOR_PALAVRAS = "palavras"
    SERVIDOR_ELASTIC_SEARCH = "elastic_search"

    # Primeiro nivel
    LOG = "logger"
    FRASES = "frases"
    SINONIMOS = "sinonimos"
    SERVIDORES = "servidores"
    CHATTERBOT = "chatterbot"

    # Segundo nivel
    REGEX = FRASES + ".regex"
    SERVIDOR = SERVIDORES + ".{servidor}"

    # Regexps
    REGEX_VOZ_PASSIVA = REGEX + ".voz_passiva"
    REGEX_PALAVRA_VERBO = REGEX + ".palavra_verbo"
    REGEX_PALAVRA_ADJETIVO = REGEX + ".palavra_adjetivo"
    REGEX_PALAVRA_RELEVENTE = REGEX + ".palavra_relevante"
    REGEX_PALAVRA_PREPOSICAO = REGEX + ".palavra_preposicao"
    REGEX_PALAVRA_SUBSTANTIVO = REGEX + ".palavra_substantivo"

    # Lista de verbos de ligação
    VERBOS_DE_LIGACAO = FRASES + ".verbos_de_ligacao"

    # Serviços
    PORTA = SERVIDOR + ".porta"
    ENDPOINT = SERVIDOR + ".endpoint"
    SERVICOS = SERVIDOR + ".servicos"
    SERVICO = SERVICOS + ".{nome_servico}"
    CONFIGURACOES_SERVIDOR = SERVIDOR + ".settings"

    # Sinonimos
    SINONIMOS_LINGUAGENS = SINONIMOS + ".linguagens"


class PalavrasServidorConstantes:
    SERVIDOR_NOME = "palavras"

    ANALISAR_FRASE_PARAM = "frase"
    ENDPOINT = ConfiguracoesConstantes.ENDPOINT.format(servidor=SERVIDOR_NOME)
    PORTA = ConfiguracoesConstantes.PORTA.format(servidor=SERVIDOR_NOME)
    SERVICO_ANALISAR_FRASE = ConfiguracoesConstantes.SERVICO.format(
            servidor=SERVIDOR_NOME,
            nome_servico="analisar_frase"
    )


class LoggerConstantes:
    # Keys
    LOGGER = ConfiguracoesConstantes.LOG
    MODULOS = LOGGER + ".modulos"
    NIVEL_LOG = ".nivel"

    # Default logger
    DEFAULT_LOGGER_NIVEL = LOGGER + ".default_logger_nivel"

    # Configurações básicas do logger
    NOME_DO_ARQUIVO = LOGGER + ".nome_arquivo"
    MODO_DO_ARQUIVO = LOGGER + ".modo_arquivo"
    FORMATO = LOGGER + ".formato"

    # Lista de modulos
    MODULO_NLU = "nlu"
    MODULO_VOZ = MODULO_NLU + ".voz"
    MODULO_ARVORE = "arvore"
    MODULO_SERVICOS = "servicos"
    MODULO_SINONIMOS = "sinonimos"
    MODULO_TIPO_FRASES = MODULO_NLU + ".tipo_frases"
    MODULO_CONFIGURACOES = "configuracoes"
    MODULO_LOCUCAO_VERBAL = MODULO_NLU + ".locucao_verbal"
    MODULO_PALAVRAS_SERVICE = MODULO_SERVICOS + ".palavras_service"
    MODULO_CHATTERBOT_HELPER = MODULO_TIPO_FRASES + ".chatterbot_helper"
    MODULO_COMPLEMENTOS_NOMINAIS = MODULO_NLU + ".complementos_nominais"

    # Nivel de logs por modulo
    NIVEL_LOG_MODULO = MODULOS + ".{modulo}" + NIVEL_LOG

    # Valor para utilizar no logging.getLogger
    GET_LOGGER_MODULO = "ensepro.{modulo}"

    @classmethod
    def get_logger(cls, modulo):
        import logging
        from ensepro import configuracoes
        logger = logging.getLogger(cls.GET_LOGGER_MODULO.format(modulo=modulo))
        logger.setLevel(logging.getLevelName(configuracoes.get_config(cls.NIVEL_LOG_MODULO, path_params={"modulo": modulo})))
        return logger

    @classmethod
    def default_logger(cls):
        import logging
        from ensepro import configuracoes
        logger = logging.getLogger("ensepro")
        logger.setLevel(logging.getLevelName(configuracoes.get_config(cls.DEFAULT_LOGGER_NIVEL)))
        return logger


class ChaterbotConstantes:
    # Keys
    CONFIGURACOES = ConfiguracoesConstantes.CHATTERBOT + ".configuracoes"
    TREINAMENTO = ConfiguracoesConstantes.CHATTERBOT + ".treinamento"

    # Configurações
    NOME = CONFIGURACOES + ".name"
    TRAINER = CONFIGURACOES + ".trainer"
    LOGIC_ADAPTERS = CONFIGURACOES + ".logic_adapters"
    STORAGE_ADAPTER = CONFIGURACOES + ".storage_adapter"

    # Termos
    TIPO_DESCONHECIDO = "desconhecido"
