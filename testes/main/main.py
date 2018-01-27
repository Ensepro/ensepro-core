"""
@project ensepro
@since 24/01/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import ensepro
from ensepro import configuracoes
from ensepro.constantes import ConfiguracoesConstantes, StringConstantes


def carregar_frases():
    with open(
            configuracoes.get_config(ConfiguracoesConstantes.ARQUIVO_FRASES),
            StringConstantes.FILE_READ_ONLY,
            encoding=StringConstantes.UTF_8) as frases:

        for frase in frases:
            frase = frase.replace(StringConstantes.BREAK_LINE, "")
            if not frase or frase.startswith("#"):
                continue

            lista_frases.append(frase)


def _print(msg):
    print(msg, file=RESULT_FILE)


SEPARATOR = 200
lista_frases = ["Qual é o melhor e o pior momento da sua vida?"]
# carregar_frases()
with open("resultado.txt", StringConstantes.FILE_WRITE_ONLY, encoding=StringConstantes.UTF_8) as RESULT_FILE:
    _print("#" * SEPARATOR)
    for frase_text in lista_frases:
        frase = ensepro.analisar_frase(frase_text)

        _print("Frase {0}: {1}".format(frase.id, frase_text))
        print("Frase {0}: {1}".format(frase.id, frase_text))

        if frase.complementos_nominais:
            i = 0
            for complemento_nominal in frase.complementos_nominais:
                _print("CN {0}: {1} + {2}".format(i, complemento_nominal.nome.palavra_original, complemento_nominal.complemento.palavra_original))
                i+=1
        else:
            _print("nenhuma complementação nominal encontrada.")

        _print(frase.arvore.to_nltk_tree().pretty_print(stream=RESULT_FILE))
        _print("#" * SEPARATOR)
        RESULT_FILE.flush()