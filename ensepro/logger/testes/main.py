"""
@project ensepro
@since 03/01/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import logging
import logging.config

# load my module
from ensepro.logger.testes import my_module

# load the logging configuration
logging.config.fileConfig('logging.ini')

my_module.foo()
bar = my_module.Bar()
bar.bar()
