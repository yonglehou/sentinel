from pytc import *
import bson

class BSONHDB(HDB):
    def __getitem__(self, key):
        return bson.loads(HDB.__getitem__(self, key))
    def __setitem__(self, key, value):
        return HDB.__setitem__(self, key, bson.dumps(value))
    def get(self, key):
        return bson.dumps(HDB.get(self,key))
    def put(self, key, value):
        return HDB.put(self, key, bson.dumps(value))

def save_system_status(system_status):
    hdb = BSONHDB()

#    hdb.tune(0,-1,-1,0)
#    hdb.setcache(0,0,0)
#    hdb.setxmsiz(0)
#    hdb.setdfunit(0)

    hdb.open('system_status.tch', HDBOWRITER | HDBOCREAT)
    hdb[system_status.datetime] = system_status.to_hash()

    hdb.close()
