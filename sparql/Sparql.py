"""
@project ensepro
@since 20/07/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import json
import configuracoes
from concurrent import futures
from bean.Palavra import Palavra
from constantes.StringConstantes import UTF_8
from constantes.StringConstantes import BREAK_LINE
from constantes.ConfiguracoesConstantes import SERVIDOR_VIRTUOSO
from SPARQLWrapper import SPARQLWrapper, JSON


triplas = {}
queries = {}


def _loadQueries():
    fileQueries = configuracoes.getSparqlQueries()
    for key in fileQueries:
        query = open("../"+fileQueries[key], 'r', encoding=UTF_8).read()
        query = query.replace(BREAK_LINE, " ")
        queries[key] = query

    return queries


#TODO REVIEW verificar se é necessário fazer este método ser THREAD-SAFE.
# LIST.APPEND é THREAD-SAFe
def _salvarResultado(_triplas, dadosPalavra):
    if dadosPalavra["palavraPai"] not in triplas:
        triplas[dadosPalavra["palavraPai"]] = {}

    if dadosPalavra["lang"] not in triplas[dadosPalavra["palavraPai"]]:
        triplas[dadosPalavra["palavraPai"]][dadosPalavra["lang"]] = {}

    if dadosPalavra["palavra"] not in triplas[dadosPalavra["palavraPai"]][dadosPalavra["lang"]]:
        triplas[dadosPalavra["palavraPai"]][dadosPalavra["lang"]][dadosPalavra["palavra"]] = {}

    if dadosPalavra["tipo_consulta"] not in triplas[dadosPalavra["palavraPai"]][dadosPalavra["lang"]][dadosPalavra["palavra"]]:
        triplas[dadosPalavra["palavraPai"]][dadosPalavra["lang"]][dadosPalavra["palavra"]][dadosPalavra["tipo_consulta"]] = _triplas


def _worker(task):
    print(task)
    #prepara SPARQLWrapper
    _sparql = SPARQLWrapper(configuracoes.getServidorEndpoint(SERVIDOR_VIRTUOSO))
    _sparql.setQuery(task["query"])
    _sparql.setReturnFormat(JSON)

    #Execute a query no virutoso
    resultado = _sparql.query().convert()

    #Lista que vai arrmazenar as triplas retornadas
    _triplas = []

    #Obtem as triplas retornadas
    for result in resultado["results"]["bindings"]:
        tripla = [result["s"]["value"], result["p"]["value"], result["o"]["value"]]
        _triplas.append(tripla)

    #Salva as triplas resultantes
    _salvarResultado(_triplas, task["dados_palavra"])



def _criarTarefa(wordToSearch : str, palavraPai: str, query : str, queryKey, lang : str):
    task = {}
    task["query"] = query.replace("WORD", wordToSearch)
    task["dados_palavra"] = {}
    task["dados_palavra"]["palavra"] = wordToSearch
    task["dados_palavra"]["palavraPai"] = palavraPai
    task["dados_palavra"]["lang"] = lang
    task["dados_palavra"]["tipo_consulta"] = queryKey
    return task


def _criarTarefasParaPalavra(palavra : Palavra):
    tasks = []
    for key in queries:
        task = _criarTarefa(palavra.palavraCanonica, palavra.palavraCanonica, queries[key], key, "por")
        tasks.append(task)

    return tasks

def _criarTarefasParaSinonimos(palavra : Palavra):
    sinonimos = palavra.getSinonimos()
    tasks = []
    for lang in sinonimos:
        for word in sinonimos[lang]:
            for queryKey in queries:
                task = _criarTarefa(word, palavra.palavraCanonica, queries[queryKey], queryKey, lang)
                tasks.append(task)

    return tasks

def _criarTarefas(palavrasRelevantes : list):
    #palavra -> lang -> tipo_consulta -> triplas
    # task: {
    #     query: "SELECT .........",
    #     dados: {
    #         "palavra"
    #         "lang"
    #         "triplas"
        #     "tipo_consulta": subject OU predicate OU object   (é o queryKey, ou seja, o nome da configuração de queries)
    #     }
    # }

    tasks = []
    for palavra in palavrasRelevantes:
        tasks = tasks + _criarTarefasParaPalavra(palavra)
        tasks = tasks + _criarTarefasParaSinonimos(palavra)

    return tasks


def consular(fraseProcessada):
    tarefas = _criarTarefas(fraseProcessada["palavras_relevantes"])

    # Run tasks.
    with futures.ThreadPoolExecutor(10) as executor:
        executor.map(_worker, tarefas)

    with open("../__ignorar/temp.json", 'a', encoding="utf8") as out:
        out.write(json.dumps(triplas, ensure_ascii=False, indent=2))


_loadQueries()




