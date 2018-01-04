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
    TIPO_FRASES = "tipos_frases"

    # Segundo nivel
    REGEX = FRASES + ".regex"
    SERVIDOR = SERVIDORES + ".{servidor}"

    # Arquivo que contém as frases
    ARQUIVO_FRASES = FRASES + ".arquivo"

    # Regexps
    REGEX_VOZ_PASSIVA = REGEX + ".voz_passiva"
    REGEX_PALAVRA_VERBO = REGEX + ".palavra_verbo"
    REGEX_PALAVRA_ADJETIVO = REGEX + ".palavra_adjetivo"
    REGEX_PALAVRA_RELEVENTE = REGEX + ".palavra_relevante"
    REGEX_PALAVRA_PREPOSICAO = REGEX + ".palavra_preposicao"
    REGEX_PALAVRA_SUBSTANTIVO = REGEX + ".palavra_substantivo"

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
