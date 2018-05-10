# -*- coding: utf-8 -*-
"""
@project ensepro
@since 25/02/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import re
from ensepro import configuracoes
from ensepro.classes.classe_gramatical import ClasseGramatical
from ensepro.constantes import ConfiguracoesConstantes
from ensepro.conversores import make_json_serializable

regex_palavra_verbo = re.compile(configuracoes.get_config(ConfiguracoesConstantes.REGEX_PALAVRA_VERBO))
regex_palavra_adjetivo = re.compile(configuracoes.get_config(ConfiguracoesConstantes.REGEX_PALAVRA_ADJETIVO))
regex_palavra_preposicao = re.compile(configuracoes.get_config(ConfiguracoesConstantes.REGEX_PALAVRA_PREPOSICAO))
regex_palavra_substantivo = re.compile(configuracoes.get_config(ConfiguracoesConstantes.REGEX_PALAVRA_SUBSTANTIVO))
regex_palavra_substantivo_proprio = re.compile(configuracoes.get_config(ConfiguracoesConstantes.REGEX_PALAVRA_SUBSTANTIVO_PROPRIO))


class Palavra:

    def __init__(self, id=None, dados_palavra=None):
        self.id = id
        self.tags = dados_palavra["tags"] if dados_palavra else None
        self.nivel = int(dados_palavra["nivel"]) if dados_palavra else None
        self.tag_inicial = dados_palavra["tag_inicial"] if dados_palavra else None
        self.palavra_original = dados_palavra["palavra_original"] if dados_palavra else None
        self.palavra_canonica = dados_palavra["palavra_canonica"] if dados_palavra else None
        self.__sinonimos = None
        self.__classe_gramatical = None

    @property
    def sinonimos(self):
        if self.__sinonimos:
            return self.__sinonimos

        from ensepro import sinonimos, configuracoes
        from ensepro.sinonimos import Sinonimo
        from ensepro.constantes import ConfiguracoesConstantes
        linguagens = configuracoes.get_config(ConfiguracoesConstantes.SINONIMOS_LINGUAGENS)
        self.__sinonimos = {}

        for linguagem in linguagens:
            lista_sinonimo_string = sinonimos.get_sinonimos(self.palavra_canonica, linguagem)
            lista_sinonimos = Sinonimo.from_list_string(lista_sinonimo_string)
            self.__sinonimos[linguagem] = list(
                    set([sinonimo for sinonimo in lista_sinonimos if sinonimo.classe_gramatical == self.classe_gramatical]))

        return self.__sinonimos

    @property
    def classe_gramatical(self):
        if self.__classe_gramatical:
            return self.__classe_gramatical
        self.__classe_gramatical = ClasseGramatical.classe_gramatical_palavra(self)
        return self.__classe_gramatical

    def is_verbo(self):
        return bool(regex_palavra_verbo.search(self.tag_inicial))

    def is_adjetivo(self):
        return bool(regex_palavra_adjetivo.search(self.tag_inicial))

    def is_preposicao(self):
        return bool(regex_palavra_preposicao.search(self.tag_inicial))

    def is_substantivo(self):
        return bool(regex_palavra_substantivo.search(self.tag_inicial))

    def is_substantivo_proprio(self):
        return bool(regex_palavra_substantivo_proprio.search(self.tag_inicial))

    def __to_json__(self):
        return {
            "id": self.id,
            "tag_inicial": self.tag_inicial,
            "palavra_original": self.palavra_original,
            "palavra_canonica": self.palavra_canonica,
            "tags": self.tags,
            "nivel": self.nivel,
            "sinonimos": self.__sinonimos
        }

    def __hash__(self):
        return hash(str(self.as_text))

    def __eq__(self, other):
        return str(self.palavra_original) == str(other.palavra_original)

    def __str__(self):
        if self.palavra_original:
            return "[{0}|{1}| {2}]".format(self.tag_inicial, self.id, self.palavra_original)
        return "{0}|{1}|".format(self.tag_inicial, self.id)

    def __repr__(self):
        return self.palavra_original

    @property
    def as_text(self) -> str:
        return \
            "Palavra={{id={0}, tags={1}, nivel={2}, tag_inicial={3}, palavra_original={4}, palavra_canonica={5}}}" \
            "".format(
                    str(self.id),
                    str(self.tags),
                    str(self.nivel),
                    str(self.tag_inicial),
                    str(self.palavra_original),
                    str(self.palavra_canonica)
            )
