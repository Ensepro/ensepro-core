"""
@project ensepro
@since 20/07/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

ENSEPRO_PATH = "../"
SAVE_FILES_TO = ENSEPRO_PATH + "__ignorar/"

LINGUAGEM_FRASES = "por"  # português

# Caminho do arquivo de configuração
ARQUIVO_CONFIGURACAO = "../configuracoes/configuracoes.json"

# Servidores
SERVIDOR_VIRTUOSO = "virtuoso"
SERVIDOR_PALAVRAS = "palavras"

# Chaves primarias
CONFIG_FRASES = "frases"
CONFIG_TIPO_FRASES = "tipos_frases"
CONFIG_SERVIDORES = "servidores"
CONFIG_SINONIMOS = "sinonimos"

# Arquivo que contém as frases
CONFIG_ARQUIVO_FRASES = CONFIG_FRASES + "/arquivo_frases"

# Regex
CONFIG_REGEX_PALAVRA_SUBSTANTIVO = CONFIG_FRASES + "/regex_palavra_substantivo"
CONFIG_REGEX_PALAVRA_PREPOSICAO = CONFIG_FRASES + "/regex_palavra_preposicao"
CONFIG_REGEX_PALAVRA_RELEVENTE = CONFIG_FRASES + "/regex_palavra_relevante"
CONFIG_REGEX_PALAVRA_ADJETIVO = CONFIG_FRASES + "/regex_palavra_adjetivo"
CONFIG_REGEX_PALAVRA_VERBO = CONFIG_FRASES + "/regex_palavra_verbo"
CONFIG_REGEX_VOZ_PASSIVA = CONFIG_FRASES + "/regex_voz_passiva"

# Serviços
CONFIG_ENDPOINT = CONFIG_SERVIDORES + "/{nome_servidor}/endpoint"
CONFIG_SERVICOS = CONFIG_SERVIDORES + "/{nome_servidor}/servicos"
CONFIG_SERVICO = CONFIG_SERVICOS + "/{nome_servico}"
CONFIG_QUERIES_SPARQL = CONFIG_SERVIDORES + "/{nome_servidor}/queries"

# Sinonimos
CONFIG_SINONIMOS_LINGUAGENS = CONFIG_SINONIMOS + "/linguagens"

# Mensagens
MENSAGEM_CARREGANDO = "Carregando configurações [{fromFile}]."
MENSAGEM_CARREGAMENTO_SUCESSO = "Configurações carregadas com sucesso."
MENSAGEM_CARREGAMENTO_ERRO = "Não foi possível carregar as configurações do arquivo json[{fromFile}]."
