"""
@project ensepro
@since 28/02/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import json
import ensepro

PT_BR = "pt_BR"


def execute(file, resultados, mostrar_sinonimos):
    qald_json = json.loads(open(file=file, mode='r', encoding="UTF-8").read())
    qald_questions = qald_json["questions"]

    frases = []

    for qald_question in qald_questions:
        if tem_pergunta_pt_br(qald_question):
            frases.append(qald_question["question"]["string"])

    ensepro.analisar_frases_and_execute(
            frases,
            __command,
            file=open(resultados, mode='w', encoding="UTF-8") if resultados else None,
            mostrar_sinonimos=mostrar_sinonimos
    )


def tem_pergunta_pt_br(qald_question):
    for lang_question in qald_question["question"]:
        if lang_question["language"] == PT_BR:
            # mantém somente a questão em português
            qald_question["question"] = lang_question
            return True
    return False


def __command(frase_analisada, *args):
    ensepro.frase_pretty_print(frase_analisada, file=args[0]["file"], mostrar_sinonimos=args[0]["mostrar_sinonimos"])
    print("#" * 150, file=args[0]["file"], end="\n\n")
