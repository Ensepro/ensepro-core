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

    frases_analisdas = ensepro.analisar_frases(frases)

    file = open(resultados + ".txt", mode='w', encoding="UTF-8") if resultados else None
    for frase_analisada in frases_analisdas:
        command(
                frase_analisada,
                file=file,
                mostrar_sinonimos=mostrar_sinonimos
        )

    print(json.dumps(frases_analisdas, indent=4, sort_keys=False, ensure_ascii=False), file=open(resultados + ".json", mode='w', encoding="UTF-8"))

def tem_pergunta_pt_br(qald_question):
    for lang_question in qald_question["question"]:
        if lang_question["language"] == PT_BR:
            # mantém somente a questão em português
            qald_question["question"] = lang_question
            return True
    return False


def command(frase_analisada, file, mostrar_sinonimos):
    ensepro.frase_pretty_print(frase_analisada, file=file, sinonimos=mostrar_sinonimos)
    print("#" * 150, file=file, end="\n\n")
