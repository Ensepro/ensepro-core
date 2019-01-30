from ensepro.constantes import LoggerConstantes

from ensepro import configuracoes
from ensepro.constantes import WordEmbedding, ConfiguracoesConstantes
from gensim.test.utils import datapath, get_tmpfile
from gensim.scripts.glove2word2vec import glove2word2vec

logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_WORD_EMBEDDING)

from gensim.models import KeyedVectors

wv = None


def init(vec: str, binary: bool, glove: bool):
    global wv
    if not vec:
        vec = configuracoes.get_config(WordEmbedding.DEFAULT_VEC_FILE)
        binary = configuracoes.get_config(WordEmbedding.DEFAULT_VEC_BINARY)
        glove = configuracoes.get_config(WordEmbedding.DEFAULT_VEC_GLOVE)

    logger.info("Carregando vetor de treinamento: %s - binary=%s, glove=%s", vec, binary, glove)
    if not glove:
        wv = KeyedVectors.load_word2vec_format(vec, binary=binary)
        return

    if glove:
        tmp_file = get_tmpfile("glove2w2v_")
        glove2word2vec(vec, tmp_file)
        wv = KeyedVectors.load_word2vec_format(tmp_file)
        return


def word_embedding(palavra1, palavra2):
    if not wv:
        return 0
    try:
        result = wv.similarity(palavra1, palavra2)
        logger.debug("Verificando similaridade entra palavras: %s - %s = %s",
                     palavra1, palavra2, result)
        return result
    except Exception as ex:
        logger.error("Erro ao verificar similaridade entre palavras [%s - %s]", palavra1, palavra2)
        # logger.exception(ex)
        return 0


if __name__ == '__main__':
    import sys

    if len(sys.argv) <= 2:
        print("São necessários pelo menos dois parametros. 'palavra1' e 'palavra2'")
        exit(1)

    palavra1 = sys.argv[1]
    palavra2 = sys.argv[2]

    print(word_embedding(palavra1, palavra2))
