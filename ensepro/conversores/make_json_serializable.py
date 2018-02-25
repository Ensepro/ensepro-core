# -*- coding: utf-8 -*-
"""
@project ensepro
@since 25/02/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

---------------------------------------------------------------------
From: https://stackoverflow.com/a/18561055/8250538

Module that monkey-patches json module when it's imported so
JSONEncoder.default() automatically checks for a special "__to_json__()"
method and uses it to encode the object if found.
"""

from json import JSONEncoder


def _default(self, obj):
    return getattr(obj.__class__, "__to_json__", _default.default)(obj)


_default.default = JSONEncoder().default  # Save unmodified default.
JSONEncoder.default = _default  # replacement
