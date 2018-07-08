import configparser
import os.path

CONFIG_LOCATION = os.path.join(os.path.dirname(__file__), 'config.ini')
conf = configparser.ConfigParser()
conf.read(CONFIG_LOCATION)

