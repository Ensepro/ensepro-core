"""
@project ensepro
@since 19/12/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""


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
    ARQUIVO_CONFIGURACOES = "./configs.json"

    # Servidores
    SERVIDOR_PALAVRAS = "palavras"
    SERVIDOR_ELASTIC_SEARCH = "elastic_search"

    # Primeiro nivel
    LOG = "logger"
    FRASES = "frases"
    SINONIMOS = "sinonimos"
    SERVIDORES = "servidores"

    # Segundo nivel
    REGEX = FRASES + ".regex"
    SERVIDOR = SERVIDORES + ".{servidor}"
    LOG_MODULOS = LOG + ".modulos"

    # Arquivo que contém as frases
    ARQUIVO_FRASES = FRASES + ".arquivo"

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
    SERVICO_ANALISAR_FRASE = ConfiguracoesConstantes.SERVICO.format(
            servidor=SERVIDOR_NOME,
            nome_servico="analisar_frase"
    )


class LoggerConstantes:
    # Keys
    LOGGER = ConfiguracoesConstantes.LOG
    MODULOS = ConfiguracoesConstantes.LOG_MODULOS
    NIVEL_LOG = ".nivel"

    # Arquivo que será salvo os logs
    NOME_DO_ARQUIVO = LOGGER + ".nome_arquivo"

    # Formato que a informação do log será exibida
    FORMATO = LOGGER + ".formato"

    # Lista de modulos
    MODULO_NLU = "nlu"
    MODULO_ARVORE = "arvore"
    MODULO_SINONIMOS = "sinonimos"
    MODULO_TIPO_FRASES = "nlu.tipo_frases"
    MODULO_CONFIGURACOES = "configuracoes"
    MODULO_COMPLEMENTOS_NOMINAIS = "nlu.complementos_nominais"

    # Nivel de logs por modulo
    NIVEL_LOG_MODULO = MODULOS + ".{modulo}" + NIVEL_LOG

    # Valor para utilizar no logging.getLogger
    GET_LOGGER_MODULO = "ensepro.{modulo}"

    # Default logger

    @classmethod
    def get_logger(cls, modulo):
        import logging
        from ensepro import configuracoes
        logger = logging.getLogger(cls.GET_LOGGER_MODULO.format(modulo=modulo))
        logger.setLevel(logging.getLevelName(configuracoes.get_config(cls.NIVEL_LOG_MODULO, path_params={"modulo": modulo})))
        return logger
