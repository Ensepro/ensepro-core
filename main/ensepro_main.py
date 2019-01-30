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
from ensepro.cbc import atualizar_frase
from ensepro.cbc import consultar
from ensepro.constantes.constantes import LoggerConstantes

if len(sys.argv) < 2:
    print("Parametro '-frase' ou '-arquivo-frases' deve ser passado. '-h' ou '--help' para ver outras opcoes.")
    exit(1)

args = main_params.get_args()

logger = LoggerConstantes.default_logger()

frases_texto = []
frases_analisadas = []
frases_reanalisadas = []
respostas = []
file = open("resultados.txt", mode="a", encoding="UTF-8") if args.save_txt else None

if args.arquivo_frases:
    if not args.quiet:
        print("Carregando frases do arquivo:", args.arquivo_frases, "...", end="", flush=True)

    frases_texto = main_utils.carregar_frases(args.arquivo_frases)

    if not args.quiet:
        print("done")

if args.frase:
    frases_texto.append(args.frase)

if not args.quiet:
    print("Analisando frase(s)... ")


def analisar(frase_texto):
    frase_final = None
    resposta = []
    frase_original = ensepro.analisar_frase(frase_texto)
    frases_analisadas.append(frase_original)

    deve_responder = (args.verbose or args.resposta) and not args.sem_resposta

    if deve_responder or args.final:
        frase_final = atualizar_frase(frase_original)
        frases_reanalisadas.append(frase_final)

    if deve_responder:
        resposta = consultar(frase_final)
        respostas.append(resposta)

    if args.save_json and not args.save_txt:
        return

    if args.original and args.final:
        main_utils.comparar_frases(ensepro, frase_original, frase_final, args, file=file)
        return

    if args.original:
        main_utils.print_frase(ensepro, frase_original, args, file=file)

    if args.final:
        main_utils.print_frase(ensepro, frase_final, args, file=file)

    if deve_responder:
        main_utils.print_resposta(ensepro, resposta, file=file)

from ensepro.servicos import word_embedding
word_embedding.init(args.word_embedding_vector, args.vec_binary, args.vec_glove)

for frase_texto in frases_texto:
    try:
        analisar(frase_texto)
    except Exception as ex:
        logger.exception(ex)
        print("\n\n{}".format(ex))
        # raise ex

if args.save_json:
    resultado_json = []
    for index in range(len(frases_analisadas)):
        json = {
            "frase_original": frases_analisadas[index]
        }
        if args.verbose or args.resposta or args.final:
            json["frase_final"] = frases_reanalisadas[index]
        if args.verbose or args.resposta:
            json["resposta"] = respostas[index]

        resultado_json.append(json)

    ensepro.save_as_json(resultado_json, "resultados.json")
