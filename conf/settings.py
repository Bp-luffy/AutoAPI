import os

CONF_PATH = os.path.dirname(__file__)
BASE_PATH = os.path.dirname(CONF_PATH)
DB_PATH = os.path.join(CONF_PATH, 'dbconfig.ini')
KFK_PATH = os.path.join(CONF_PATH, 'kfkconfig.ini')
DATA_PATH = None
# DATA_PATH = '/Users/edz/Downloads/data.csv'
