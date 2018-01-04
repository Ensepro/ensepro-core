"""
@project ensepro
@since 04/01/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

---------------------------------------------------------------------
From: https://stackoverflow.com/a/18561055/8250538

Module that monkey-patches json module when it's imported so
JSONEncoder.default() automatically checks for a special "to_json()"
method and uses it to encode the object if found.
"""

from json import JSONEncoder


def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)


_default.default = JSONEncoder().default  # Save unmodified default.
JSONEncoder.default = _default  # replacement
