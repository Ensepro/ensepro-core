"""
@project ensepro
@since 20/07/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

SERVIDOR_VIRTUOSO = "virtuoso"
SERVIDOR_PALAVRAS = "palavras"

#Configurações que deverão existir para inicializar o programa.

CONFIG_ARQUIVO_FRASES = "frases"
CONFIG_TIPO_FRASES = "tipos_frases"
CONFIG_SERVIDORES = "servidores"

CONFIG_ENDPOINT = CONFIG_SERVIDORES + "/{nome_servidor}/endpoint"
CONFIG_SERVICOS = CONFIG_SERVIDORES + "/{nome_servidor}/servicos"
CONFIG_SERVICO  = CONFIG_SERVICOS   + "/{nome_servico}"
CONFIG_QUERIES_SPARQL = CONFIG_SERVIDORES + "/{nome_servidor}/queries"


#Mensagens
MENSAGEM_ERRO = "A configuração {att} deve existir no arquivo de configuração."
MENSAGEM_CARREGANDO = "Carregando configurações [{fromFile}]."
MENSAGEM_CARREGAMENTO_SUCESSO = "Configurações carregadas com sucesso."
MENSAGEM_CARREGAMENTO_ERRO = "Não foi possível carregar as configurações do arquivo json[{fromFile}]."





