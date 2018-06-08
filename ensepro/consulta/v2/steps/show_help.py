# -*- coding: utf-8 -*-
"""
@project ensepro
@since 08/06/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""


def show_help(params, step, steps):
    print("*******************************************")
    print("********* HELPER query_generator  *********")
    print("*******************************************")

    print("-help:", "Mostre esta ajuda")

    print()

    print("-elasticsearch:", "1ª ação, inícia o processo do início. [peso default 1]")
    print("      Exemplo 1: query_generator.py -elasticsearch tr1 tr2 ... trN")
    print("      Exemplo 2: query_generator.py -elasticsearch tr1 peso1 tr2 peso2 ... trN pesoN")
    print("      Exemplo 3: query_generator.py -elasticsearch tr1 tr2 peso2 tr3")

    print()

    print("-normalizar:", "2ª ação, é executa automaticamente após a 1ª. Mas pode ser iniciada a partir do arquivo gerado na 1ª")
    print("      Exemplo: query_generator.py -normalizar ARQUIVO")
    print("      ARQUIVO default elastic_search_step.json")

    print()

    print("-gerar:", "3ª ação, é executa automaticamente após a 2ª. Mas pode ser iniciada a partir do arquivo gerado na 2ª")
    print("      Exemplo: query_generator.py -gerar ARQUIVO")
    print("      ARQUIVO default resultado_normalizado.json")

    print()

    print("-ranquear:", "4ª ação, é executa automaticamente após a 3ª. Mas pode ser iniciada a partir do arquivo gerado na 3ª")
    print("      Exemplo: query_generator.py -ranquear ARQUIVO")
    print("      ARQUIVO default gerar_queries_step.json")

    print()

    print("-printar-resultados:", "5ª ação, é executa automaticamente após a 4ª. Mas pode ser iniciada a partir do arquivo gerado na 4ª")
    print("      Exemplo: query_generator.py -printar-resultados ARQUIVO")
    print("      ARQUIVO default queries_renqueadas.json")

    print()
