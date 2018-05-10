"""
@project ensepro
@since 01/03/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""


def arquivo_existente(parser, arg):
    import os
    arg = os.path.abspath(arg)
    if os.path.exists(arg):
        return arg
    parser.error("O arquivo '%s' não existe." % arg)


def get_args():
    """
    -f, --file PATH -> indica um arquivo contendo frases a ser processado
    -s, --save PATH -> indica o arquivo onde será salvo todos os resultados
    -ms, --mostrar-sinonimos -> se presente, irá fazer a busca e mostrar dos sinonimos das palavras relevantes
    """

    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument("-f", "--file",
                        type=lambda x: arquivo_existente(parser, x),
                        required=True,
                        dest="arquivo_processar",
                        help="Arquivo QALD a ser processado, deve ser um json.")

    parser.add_argument("-s", "--save",
                        default=None,
                        dest="arquivo_resultado",
                        help="Arquivo onde os resultados serão salvos.")

    parser.add_argument("-ms", "--mostrar-sinonimos",
                        dest="mostrar_sinonimos",
                        help="Busca e salva os sinônimos dos termos relevantes.",
                        action="store_true",
                        default=False)

    return parser.parse_args()
