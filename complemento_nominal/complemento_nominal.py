"""
@project ensepro
@since 12/12/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
from utils import FraseTreeUtil
from bean.Frase import Frase


def complementos_nominais(frase):
    lista = []
    for palavra in frase.palavras:
        execute = DNs[palavra.tagInicial] if palavra.tagInicial in DNs else None
        if(execute):
            element = execute(frase, palavra)
            lista.append(element)

    return lista


def dn_adj(frase, palavra):
    complemento = palavra
    arvore_que_estou = get_arvore_que_estou(frase, palavra)
    nome = find_nucleo_arvore(arvore_que_estou)

    return build_response(nome, complemento)

def dn_prop(frase, palavra):
    return dn_adj(frase, palavra)

def dn_np(frase, palavra):
    minha_arvore = get_minha_arvore(frase, palavra)
    minha_arvore_nucleo = find_nucleo_arvore(minha_arvore)

    arvore_que_estou = get_arvore_que_estou(frase, palavra)
    arvore_que_estou_nucleo = find_nucleo_arvore(arvore_que_estou)

    return build_response(arvore_que_estou_nucleo, minha_arvore_nucleo)

def dn_pp(frase, palavra):
    arvore_que_estou = get_arvore_que_estou(frase, palavra)
    arvore_que_estou_nucleo = find_nucleo_arvore(arvore_que_estou)
    arvore_no_nao_terminal_nucleo = get_nucleo_sub_arvores(arvore_que_estou)

    return build_response(arvore_que_estou_nucleo, arvore_no_nao_terminal_nucleo)


NUCLEOS = ["H:n", "H:prop"]
DNs = {
    "DN:adj": dn_adj,
    "DN:prop": dn_prop,
    "DN:np": dn_np,
    "DN:pp": dn_pp,
}


def get_nucleo_sub_arvores(arvore):
    arvore_no_nao_terminal = get_minha_arvore(arvore, find_nodo_nao_terminal(arvore))
    arvore_no_nao_terminal_nucleo = None
    while (arvore_no_nao_terminal):
        arvore_no_nao_terminal_nucleo = find_nucleo_arvore(arvore_no_nao_terminal)
        if (arvore_no_nao_terminal_nucleo):
            break

        arvore_no_nao_terminal = get_minha_arvore(arvore_no_nao_terminal, find_nodo_nao_terminal(arvore_no_nao_terminal))

    return arvore_no_nao_terminal_nucleo


def find_nodo_nao_terminal(frase):
    for palavra in frase.palavras[1:]:
        if(FraseTreeUtil.isNoNaoTerminal(frase, palavra.numero)):
            return palavra


def build_response(nome, complemento):
    return {
        "nome": nome,
        "complemento": complemento
    }

def get_minha_arvore(frase, palavra):
    minha_arvore = [palavra]
    palavras = frase.palavras
    index = palavras.index(palavra)

    while (index + 1 < len(palavras)):
        index += 1
        __palavra = palavras[index]

        if(palavra.nivel >= __palavra.nivel):
            break

        minha_arvore.append(__palavra)

    return Frase(minha_arvore, frase.id)

def get_arvore_que_estou(frase, palavra):
    palavra_pai = find_pai(frase, palavra)
    return get_minha_arvore(frase, palavra_pai)

def find_pai(frase, palavra):
    palavras = frase.palavras
    index = palavras.index(palavra)

    while (index > 0):
        index -= 1
        __palavra = palavras[index]
        if palavra.nivel > __palavra.nivel:
            return __palavra

    return None

def find_nucleo_arvore(frase):
    for nucleo in NUCLEOS:
        for palavra in frase.palavras:
            if nucleo in palavra.tagInicial:
                return palavra

    return None
