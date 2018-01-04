"""
@project ensepro
@since 30/12/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import logging


def foo():
    logger = logging.getLogger(__name__)
    logger.info('Hi, foo')


class Bar(object):

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    def bar(self):
        self.logger.info('Hi, bar')
