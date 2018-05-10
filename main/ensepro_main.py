# -*- coding: utf-8 -*-
"""
@project ensepro
@since 09/05/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import os
import sys

# Seta no path do sistema a pasta que a pasta deste arquivo está contido
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import main_utils
from main import main_params
import ensepro

if len(sys.argv) < 2:
    print("Parametro '-frase' ou '-arquivo-frases' deve ser passado. '-h' ou '--help' para ver outras opcoes.")
    exit(1)

args = main_params.get_args()

frases_texto = []

if args.arquivo_frases:
    if not args.quiet:
        print("Carregando frases do arquivo:", args.arquivo_frases, "...", end="", flush=True)

    frases_texto = main_utils.carregar_frases(args.arquivo_frases)

    if not args.quiet:
        print("done")

if args.frase:
    frases_texto.append(args.frase)

if not args.quiet:
    print("Analisando frase(s)... ", end="", flush=True)

frases_analisadas = ensepro.analisar_frases(frases_texto)

for frase_analisada in frases_analisadas:
    t = frase_analisada.tipo
    t = frase_analisada.voz
    if args.termos_relevantes or args.verbose:
        t = frase_analisada.palavras_relevantes

    if args.sinonimos or args.verbose:
        t = frase_analisada.sinonimos

    if args.complementos_nominais or args.verbose:
        t = frase_analisada.complementos_nominais

    if args.locucoes_verbais or args.verbose:
        t = frase_analisada.locucao_verbal

    if args.arvore or args.verbose:
        t = frase_analisada.arvore

if not args.quiet:
    print("done")

if args.save_json:
    if not args.quiet:
        print("Salvando arquivo json 'resultados.json'...", end="", flush=True)

    ensepro.save_as_json(frases_analisadas, "resultados.json")

    if not args.quiet:
        print("done")

if args.save_txt:
    if not args.quiet:
        print("Salvando arquivo txt 'resultados.txt'...", end="", flush=True)

    file = open("resultados.txt", mode="w", encoding="UTF-8")
    main_utils.print_frases(ensepro, frases_analisadas, args, file=file)

    if not args.quiet:
        print("done")

if not args.save_txt and not args.save_json:
    main_utils.print_frases(ensepro, frases_analisadas, args)
