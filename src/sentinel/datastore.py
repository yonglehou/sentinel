from pytc import *
from os import *
from os.path import *
import datetime
import bson

SENTINELD_LOG_DIR = '/var/log/sentineld'

class BSONHDB(HDB):
    def __setitem__(self, key, value):
        HDB.__setitem__(self, key, bson.dumps(value))

    def __getitem__(self, key):
        return bson.loads(HDB.__getitem__(self, key))

    def put(self, key, value):
        HDB.put(self, key, bson.dumps(value))

    def get(self, key):
        return bson.loads(HDB.get(self, key))

def initialize():
    if not exists(SENTINELD_LOG_DIR):
        makedirs(SENTINELD_LOG_DIR)

def save_system_status(system_status):
    hdb = BSONHDB()

    today = datetime.date.today()
    log_file = SENTINELD_LOG_DIR + '/' + str(today.year) + str(today.month) + str(today.day) + '.tch'
    
    hdb.open(log_file, HDBOWRITER | HDBOCREAT)
    hdb[str(system_status.datetime)] = system_status.to_dict()

    hdb.close()
