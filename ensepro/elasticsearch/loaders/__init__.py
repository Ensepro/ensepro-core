"""
@project ensepro
@since 11/03/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
from .dataset import carregar_dataset




def criar_acao_insercao(index_name, index_type, source):
    return {
        "_op_type": 'index',
        "_index": index_name,
        "_type": index_type,
        "_source": source
    }