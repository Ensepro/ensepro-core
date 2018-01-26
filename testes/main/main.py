"""
@project ensepro
@since 24/01/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import ensepro
from ensepro import configuracoes
from ensepro.constantes import ConfiguracoesConstantes, StringConstantes

lista_frases = []


def carregarFrases():
    with open(
            configuracoes.get_config(ConfiguracoesConstantes.ARQUIVO_FRASES),
            StringConstantes.FILE_READ_ONLY,
            encoding=StringConstantes.UTF_8) as frases:

        for frase in frases:
            frase = frase.replace(StringConstantes.BREAK_LINE, "")
            if not frase or frase.startswith("#"):
                continue

            lista_frases.append(frase)

print("#" * 100)
carregarFrases()
for frase_text in lista_frases:
    frase = ensepro.analisar_frase(frase_text)

    print("Frase: {}".format(frase_text))
    print("Frase id={}".format(frase.id))
    print("Frase palavras_relevantes={}".format(frase.palavras_relevantes))
    # print("Frase tipo={}".format(frase.tipo))
    print("Frase voz={}".format(frase.voz))
    print("Frase locucao_verbal={}".format(frase.locucao_verbal))
    print("Frase complementos_nominais={}".format(frase.complementos_nominais))
    print(frase.arvore)
    print(frase.arvore.to_nltk_tree().pretty_print())
    print("#" * 100)
