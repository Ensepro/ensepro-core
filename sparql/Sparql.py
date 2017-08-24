"""
@project ensepro
@since 20/07/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import json
import configuracoes
from concurrent import futures
from bean.Palavra import Palavra
from constantes.SparqlConstantes import *
from constantes.NLUConstantes import PALAVRAS_RELEVANTES
from constantes.StringConstantes import UTF_8
from constantes.StringConstantes import BREAK_LINE
from constantes.StringConstantes import FILE_READ_ONLY
from constantes.StringConstantes import FILE_WRITE_ONLY
from constantes.ConfiguracoesConstantes import SERVIDOR_VIRTUOSO
from SPARQLWrapper import SPARQLWrapper, JSON

triplas = {}
queries = {}
EXECUTION_NUMBER = 1

def _loadQueries():
    fileQueries = configuracoes.getSparqlQueries()
    for key in fileQueries:
        query = open(RELATIVE_PATH + fileQueries[key], FILE_READ_ONLY, encoding=UTF_8).read()
        query = query.replace(BREAK_LINE, " ")
        queries[key] = query

    return queries


# TODO REVIEW verificar se é necessário fazer este método ser THREAD-SAFE.
# LIST.APPEND é THREAD-SAFe
def _salvarResultado(_triplas, dadosPalavra):
    if dadosPalavra[PALAVRA_PAI] not in triplas:
        triplas[dadosPalavra[PALAVRA_PAI]] = {}

    if dadosPalavra[LANG] not in triplas[dadosPalavra[PALAVRA_PAI]]:
        triplas[dadosPalavra[PALAVRA_PAI]][dadosPalavra[LANG]] = {}

    if dadosPalavra[PALAVRA] not in triplas[dadosPalavra[PALAVRA_PAI]][dadosPalavra[LANG]]:
        triplas[dadosPalavra[PALAVRA_PAI]][dadosPalavra[LANG]][dadosPalavra[PALAVRA]] = {}

    if dadosPalavra[TIPO_CONSULTA] not in triplas[dadosPalavra[PALAVRA_PAI]][dadosPalavra[LANG]][dadosPalavra[PALAVRA]]:
        triplas[dadosPalavra[PALAVRA_PAI]][dadosPalavra[LANG]][dadosPalavra[PALAVRA]][dadosPalavra[TIPO_CONSULTA]] = _triplas


def _worker(task):
    # print(task)
    # prepara SPARQLWrapper
    _sparql = SPARQLWrapper(configuracoes.getUrlService(SERVIDOR_VIRTUOSO, SPARQL_NOME_SERVICO))
    _sparql.setQuery(task[QUERY])
    _sparql.setReturnFormat(JSON)

    # Execute a query no virutoso
    resultado = _sparql.query().convert()

    # Lista que vai arrmazenar as triplas retornadas
    _triplas = []

    # Obtem as triplas retornadas
    for result in resultado["results"]["bindings"]:
        tripla = [result["s"]["value"], result["p"]["value"], result["o"]["value"]]
        _triplas.append(tripla)

    # Salva as triplas resultantes
    _salvarResultado(_triplas, task[DADOS_PALAVRA])


def _criarTarefa(palavra: str, palavraPai: str, query: str, tipo_consulta: str, lang: str):
    task = {}
    task[QUERY] = query.replace(QUERY_ELEMENTO, palavra)
    task[DADOS_PALAVRA] = {}
    task[DADOS_PALAVRA][PALAVRA] = palavra
    task[DADOS_PALAVRA][PALAVRA_PAI] = palavraPai
    task[DADOS_PALAVRA][LANG] = lang
    task[DADOS_PALAVRA][TIPO_CONSULTA] = tipo_consulta
    return task


def _criarTarefasParaPalavra(palavra: Palavra):
    tasks = []
    for key in queries:
        task = _criarTarefa(palavra.palavraCanonica, palavra.palavraCanonica, queries[key], key, "por")
        tasks.append(task)

    return tasks


def _criarTarefasParaSinonimos(palavra: Palavra):
    sinonimos = palavra.getSinonimos()
    tasks = []
    for lang in sinonimos:
        for sinonimo in sinonimos[lang]:
            for queryKey in queries:
                task = _criarTarefa(sinonimo.sinonimo, palavra.palavraCanonica, queries[queryKey], queryKey, lang)
                tasks.append(task)

    return tasks


def _criarTarefas(palavrasRelevantes: list):
    tasks = []
    for palavra in palavrasRelevantes:
        tasks = tasks + _criarTarefasParaPalavra(palavra)
        tasks = tasks + _criarTarefasParaSinonimos(palavra)

    return tasks


def consular(fraseProcessada, FRASE_ID):
    global triplas
    triplas = {}
    print("CONSULTA_SPARQL - criando tasks...")

    tarefas = _criarTarefas(fraseProcessada[PALAVRAS_RELEVANTES])

    print("CONSULTA_SPARQL - tasks criadas.[" + str(len(tarefas)) + "]")


    print("CONSULTA_SPARQL - executando tasks...")

    print("CONSULTA_SPARQL - salvando tasks em arquivo json...")
    with open("../__ignorar/sparql_tasks_" + str(FRASE_ID) + ".json", FILE_WRITE_ONLY, encoding=UTF_8) as out:
        out.write(json.dumps(tarefas, ensure_ascii=False, indent=2))
    print("CONSULTA_SPARQL - tasks salvas.")

    # Run tasks.
    # TODO verificar quantidade de threads a serem utilizadas.
    with futures.ThreadPoolExecutor(10) as executor:
        executor.map(_worker, tarefas)


    print("CONSULTA_SPARQL - tasks executadas")
    print("CONSULTA_SPARQL - salvando resultados em arquivo json")

    with open("../__ignorar/sparql_consulta_" + str(FRASE_ID) + ".json", FILE_WRITE_ONLY, encoding=UTF_8) as out:
        out.write(json.dumps(triplas, ensure_ascii=False, indent=2))

_loadQueries()
