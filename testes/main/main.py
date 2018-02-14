"""
@project ensepro
@since 02/02/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import ensepro

frases = [
    "quem são os acadêmicos envolvidos com web semântica?",
    "Que alunos do Pipca trabalham no projeto CNJ Acadêmico patrocinados pela Capes?"
    # "Como é que a gente sabe que a carne de chester é de chester se nunca ninguém viu um chester?",
    # "Já fez alguma coisa que teve vontade de sair gritando na rua?"
]


def __command(frase_analisada, *args):
    ensepro.frase_pretty_print(frase_analisada, file=args[0]["file"])
    print("#" * 150, file=args[0]["file"], end="\n\n")


def carregar_frases():
    global frases
    frases = []
    with open("../../arquivos/frases/frases.txt", encoding="UTF-8") as frases_in_text:
        for frase in frases_in_text:
            frase = frase.replace("\n", "")

            if not frase:
                continue

            if frase.startswith("#"):
                continue

            frases.append(frase)


carregar_frases()

with open("resultado_completo.txt", mode="w", encoding="UTF-8") as save_in:
    ensepro.analisar_frases_and_execute(frases, __command, file=save_in)
    
# ensepro.analisar_frases_and_execute(frases, __command, file=None)
