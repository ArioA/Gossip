import logging

from . import conf


FORMAT = '%(asctime)-15s %(levelname)-8s %(name)-12s %(message)s'

def init_logging():
    logging.basicConfig(
            filename=conf['GENERAL']['log_file'],
            filemode='a',
            format=FORMAT,
            style='%',
            level=logging.INFO)

