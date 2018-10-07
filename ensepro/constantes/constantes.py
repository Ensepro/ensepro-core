# -*- coding: utf-8 -*-
"""
@project ensepro
@since 25/02/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""


# TODO refactor this
# TODO refactor this

def ensepro_path():
    import os
    # Obtém o PATH para a pasta que contém este arquivo
    this_file_directory = os.path.dirname(os.path.abspath(__file__))

    # Volta duas pastas
    ensepro_path = os.path.dirname(this_file_directory)
    ensepro_path = os.path.dirname(ensepro_path)

    return ensepro_path


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
    ENSEPRO_PATH = ensepro_path()
    ARQUIVO_CONFIGURACOES = ENSEPRO_PATH + "/ensepro/configuracoes/configs.json"

    # Primeiro nivel
    LOG = "logger"
    FRASES = "frases"
    SINONIMOS = "sinonimos"
    SERVIDORES = "servidores"
    CHATTERBOT = "chatterbot"
    CONSULTA = "cbc"

    # Segundo nivel
    REGEX = FRASES + ".regex"
    SERVIDOR = SERVIDORES + ".{servidor}"

    # Regexps
    REGEX_VOZ_PASSIVA = REGEX + ".voz_passiva"
    REGEX_PALAVRA_VERBO = REGEX + ".palavra_verbo"
    REGEX_PALAVRA_ADJETIVO = REGEX + ".palavra_adjetivo"
    REGEX_TERMO_RELEVANTE = REGEX + ".termo_relevante"
    REGEX_PALAVRA_PREPOSICAO = REGEX + ".palavra_preposicao"
    REGEX_PALAVRA_SUBSTANTIVO = REGEX + ".palavra_substantivo"
    REGEX_PALAVRA_SUBSTANTIVO_PROPRIO = REGEX + ".palavra_substantivo_proprio"

    # Lista de verbos de ligação
    VERBOS_DE_LIGACAO = FRASES + ".verbos_de_ligacao"
    TERMOS_RELEVANTES = FRASES + ".termos_relevantes"
    ARQUIVO_NOMINALIZACAO = FRASES + ".nominalizacao"
    TERMOS_RELEVANTES_IGNORAR = TERMOS_RELEVANTES + ".ignorar"

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

    ENDPOINT = ConfiguracoesConstantes.ENDPOINT.format(servidor=SERVIDOR_NOME)
    PORTA = ConfiguracoesConstantes.PORTA.format(servidor=SERVIDOR_NOME)

    ANALISAR_FRASE_PARAM = "frase"
    SERVICO_ANALISAR_FRASE = ConfiguracoesConstantes.SERVICO.format(
        servidor=SERVIDOR_NOME,
        nome_servico="analisar_frase"
    )


class ElasticSearchConstantes:
    SERVIDOR_NOME = "elastic_search"

    ENDPOINT = ConfiguracoesConstantes.ENDPOINT.format(servidor=SERVIDOR_NOME)
    PORTA = ConfiguracoesConstantes.PORTA.format(servidor=SERVIDOR_NOME)

    USERNAME = (ConfiguracoesConstantes.CONFIGURACOES_SERVIDOR + ".username").format(servidor=SERVIDOR_NOME)
    PASSWORD = (ConfiguracoesConstantes.CONFIGURACOES_SERVIDOR + ".password").format(servidor=SERVIDOR_NOME)
    INDEX_NAME = (ConfiguracoesConstantes.CONFIGURACOES_SERVIDOR + ".index_name").format(servidor=SERVIDOR_NOME)
    INDEX_TYPE = (ConfiguracoesConstantes.CONFIGURACOES_SERVIDOR + ".index_type").format(servidor=SERVIDOR_NOME)


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
    MODULO_CLN = "cln"
    MODULO_CBC = "cbc"
    MODULO_VOZ = MODULO_CLN + ".voz"
    MODULO_ARVORE = "arvore"
    MODULO_SERVICOS = "servicos"
    MODULO_SINONIMOS = "sinonimos"
    MODULO_CONSULTA = "consulta"
    MODULO_TIPO_FRASES = MODULO_CLN + ".tipo_frases"
    MODULO_NOMINALIZACAO = MODULO_CLN + ".nominalizacao"
    MODULO_CONFIGURACOES = "configuracoes"
    MODULO_LOCUCAO_VERBAL = MODULO_CLN + ".locucao_verbal"
    MODULO_PALAVRAS_SERVICE = MODULO_SERVICOS + ".palavras_service"
    MODULO_TERMOS_RELEVANTES = MODULO_CLN + ".termos_relevantes"
    MODULO_CHATTERBOT_HELPER = MODULO_TIPO_FRASES + ".chatterbot_helper"
    MODULO_COMPLEMENTOS_NOMINAIS = MODULO_CLN + ".complementos_nominais"
    MODULO_DBPEDIA_SPOTLIGHT_SERVICE = MODULO_SERVICOS + ".dbpedia_spotlight_service"
    MODULO_KNOWLEDGE_GRAPH_SEARCH_SERVICE = MODULO_SERVICOS + ".knowledge_graph_search_service"

    MODULO_ELASTIC_SEARCH = "elasticsearch"
    MODULO_ES_CONNECTION = MODULO_ELASTIC_SEARCH + ".connection"
    MODULO_ES_CONSULTA = MODULO_ELASTIC_SEARCH + ".searches"
    MODULO_ES_HELPERS = MODULO_ELASTIC_SEARCH + ".helpers"
    MODULO_ES_LOADERS = MODULO_ELASTIC_SEARCH + ".loaders"
    MODULO_ES_QUERIES = MODULO_ELASTIC_SEARCH + ".queries"
    MODULO_ES_DATASET = MODULO_ES_LOADERS + ".dataset"

    # Nivel de logs por modulo
    NIVEL_LOG_MODULO = MODULOS + ".{modulo}" + NIVEL_LOG

    # Valor para utilizar no logging.getLogger
    GET_LOGGER_MODULO = "ensepro.{modulo}"

    @classmethod
    def get_logger(cls, modulo):
        import logging
        from ensepro import configuracoes
        logger = logging.getLogger(cls.GET_LOGGER_MODULO.format(modulo=modulo))
        logger.setLevel(
            logging.getLevelName(configuracoes.get_config(cls.NIVEL_LOG_MODULO, path_params={"modulo": modulo})))
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
    SHOW_TRAINING_PROGRESS = CONFIGURACOES + ".show_training_progress"
    READ_ONLY = CONFIGURACOES + ".read_only"

    # Termos
    TIPO_DESCONHECIDO = "desconhecido"


class DBPediaSpotlightConstantes:
    SERVIDOR_NOME = "dbpedia_spotlight"

    ENDPOINT = ConfiguracoesConstantes.ENDPOINT.format(servidor=SERVIDOR_NOME)

    SERVICO_SPOTLIGHT = ConfiguracoesConstantes.SERVICO.format(
        servidor=SERVIDOR_NOME,
        nome_servico="spotlight"
    )

    CONFIANCAS = ConfiguracoesConstantes.SERVIDOR.format(servidor=SERVIDOR_NOME) + ".confiancas"


class KnowledgeGraphSearchConstantes:
    SERVIDOR_NOME = "knowledge_graph_search"

    API_KEY = ConfiguracoesConstantes.SERVIDOR.format(servidor=SERVIDOR_NOME) + ".key_file"
    ENDPOINT = ConfiguracoesConstantes.ENDPOINT.format(servidor=SERVIDOR_NOME)
    SEARCH_SERVICE = ConfiguracoesConstantes.SERVICO.format(
        servidor=SERVIDOR_NOME,
        nome_servico="search"
    )


class ConsultaConstantes:
    PESOS = ConfiguracoesConstantes.CONSULTA + ".pesos"

    PESOS_CLASSES = PESOS + ".classes"
    PESOS_METRICAS = PESOS + ".metricas"

    PESO_VERBO = PESOS_CLASSES + ".verbo"
    PESO_VERBO_SINONIMO = PESOS_CLASSES + ".verbo_sinonimo"
    PESO_VERBO_NOMILIZADO = PESOS_CLASSES + ".verbo_nomilizado"
    PESO_SUBSANTIVO_COMUM = PESOS_CLASSES + ".substantivo_comum"
    PESO_SUBSANTIVO_PROPRIO = PESOS_CLASSES + ".substantivo_proprio"
    PESO_SUBSANTIVO_COMUM_SINONIMO = PESOS_CLASSES + ".substantivo_comum_sinonimo"
    PESO_VERBO_NOMILIZADO_SINONIMO = PESOS_CLASSES + ".verbo_nomilizado_sinonimo"

    PESO_M1 = PESOS_METRICAS + ".m1"
    PESO_M2 = PESOS_METRICAS + ".m2"
    PESO_M3 = PESOS_METRICAS + ".m3"

    NUMERO_RESPOSTAS = ConfiguracoesConstantes.CONSULTA + ".numero_respostas"
    RESULTADO_RESUMIDO = ConfiguracoesConstantes.CONSULTA + ".resultado_resumido"
    REMOVER_RESULTADOS = ConfiguracoesConstantes.CONSULTA + ".remover_variaveis"
