# -*- coding: utf-8 -*-
"""
@project ensepro
@since 09/05/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""


def arquivo_existente(parser, arg):
    import os
    arg = os.path.abspath(arg)
    if os.path.exists(arg):
        return arg
    parser.error("O arquivo '%s' não existe." % arg)


def get_args():
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument("-frase",
                        default=None,
                        type=str,
                        dest="frase",
                        help="Frase a ser analisada.")

    parser.add_argument("-arquivo-frases",
                        default=None,
                        type=lambda x: arquivo_existente(parser, x),
                        dest="arquivo_frases",
                        help="Arquivo contento frases a serem analisadas.")

    parser.add_argument("-save-json",
                        dest="save_json",
                        help="Salvará os resultdos em um arquivo json.",
                        action="store_true",
                        default=False)

    parser.add_argument("-save-txt",
                        dest="save_txt",
                        help="Salvará os resultdos em um arquivo txt.",
                        action="store_true",
                        default=False)

    parser.add_argument("-tr",
                        dest="termos_relevantes",
                        help="Indica para printar/salvar os termos relevantes.",
                        action="store_true",
                        default=False)

    parser.add_argument("-sin",
                        dest="sinonimos",
                        help="Indica para printar/salvar os sinonimos dos termos relevantes.",
                        action="store_true",
                        default=False)

    parser.add_argument("-cn",
                        dest="complementos_nominais",
                        help="Indica para printar/salvar os complementos nominais.",
                        action="store_true",
                        default=False)

    parser.add_argument("-lv",
                        dest="locucoes_verbais",
                        help="Indica para printar/salvar os locucoes verbais.",
                        action="store_true",
                        default=False)

    parser.add_argument("-arvore",
                        dest="arvore",
                        help="Indica para printar/salvar a arvore gráfica da frase.",
                        action="store_true",
                        default=False)

    parser.add_argument("-tags",
                        dest="tags",
                        help="Indica para printar/salvar os as tags das frases no arquivo txt.",
                        action="store_true",
                        default=False)

    parser.add_argument("-resposta",
                        dest="resposta",
                        help="Indica se deve buscar uma resposta.",
                        action="store_true",
                        default=False)

    parser.add_argument("-verbose",
                        dest="verbose",
                        help="Indica para printar/salvar todos os valores existentes.",
                        action="store_true",
                        default=False)

    parser.add_argument("-quiet",
                        dest="quiet",
                        help="Indica para não printar nada enquanto faz a execução.",
                        action="store_true",
                        default=False)

    parser.add_argument("-original",
                        dest="original",
                        help="Define que os resultados são referentes a frase passada por parâmetro.",
                        action="store_true",
                        default=False)

    parser.add_argument("-final",
                        dest="final",
                        help="Define que os resultados são referentes a frase final, depois de passar pelo modulo CBC e ser atualizada.",
                        action="store_true",
                        default=False)

    return parser.parse_args()
