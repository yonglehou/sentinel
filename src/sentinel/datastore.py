from pytc import *
from os import *
from os.path import *
import datetime
import time
import bson

SENTINELD_LOG_DIR = '/var/log/sentineld'

class SystemStatus:
    def __init__(self):
        self.timestamp = int(time.time())
        self.os_type = ''
        self.os_version = ''
        self.uptime = 0
        self.idletime = 0
        self.cpu_total = None
        self.cpu_usages = []
        self.memory_total = 0
        self.memory_free = 0
        self.swap_total = 0
        self.swap_free = 0
        self.processes = []
        self.blockdevs = []
        self.netdevs = []

    def to_dict(self):
        dict_processes = [p.to_dict() for p in self.processes]
        blockdevs = [b.to_dict() for b in self.blockdevs]
        netdevs = [n.to_dict() for n in self.netdevs]
        return {
            'timestamp': self.timestamp,
            'os_type' : self.os_type,
            'os_version' : self.os_version,
            'uptime': self.uptime,
            'idletime': self.idletime,
            'cpu_total': self.cpu_total,
            'cpu_usages': self.cpu_usages,
            'memory_total': self.memory_total,
            'memory_free': self.memory_free,
            'swap_total': self.swap_total,
            'swap_free': self.swap_free,
            'processes': dict_processes,
            'blockdevs': blockdevs,
            'netdevs': netdevs,
            }

class RuntimeProcess:
    def __init__(self):
        self.pid = 0
        self.name = ''
        self.state = ''
        self.utime = 0
        self.stime = 0
        self.memory = 0
    
    def __str__(self):
        return '%d %s %s %d %d %d' % (self.pid, self.name, self.state, self.utime, self.stime, self.memory)
    
    def to_dict(self):
        return {
            'pid': self.pid,
            'name': self.name,
            'state': self.state,
            'utime': self.utime,
            'stime': self.stime,
            'memory': self.memory
            }

class BlockDevice:
    def __init__(self):
        self.device = ''
        self.read = ''
        self.write = ''
    
    def to_dict(self):
        return {
            'device': self.device,
            'read': self.read,
            'write': self.write,
            }

class NetworkDevice:
    def __init__(self):
        self.device = ''
        self.send = ''
        self.receive = ''

    def to_dict(self):
        return {
            'device': self.device,
            'send': self.send,
            'receive': self.receive,
            }


class BSONBDB(BDB):
    def __setitem__(self, key, value):
        BDB.__setitem__(self, key, bson.dumps(value))

    def __getitem__(self, key):
        return bson.loads(BDB.__getitem__(self, key))

    def put(self, key, value):
        BDB.put(self, key, bson.dumps(value))

    def get(self, key):
        return bson.loads(BDB.get(self, key))
    
    def values(self):
        result = []
        for v in BDB.values(self):
            result.append(bson.loads(v))
        return result

def initialize():
    if not exists(SENTINELD_LOG_DIR):
        makedirs(SENTINELD_LOG_DIR)

def load_system_status(target_date):
    bdb = BSONBDB()

    log_file = SENTINELD_LOG_DIR + '/' + str(target_date.year) + str(target_date.month) + str(target_date.day) + '.db'
    bdb.open(log_file, BDBOREADER | BDBOCREAT)

    result = []
    for entry in bdb.values():
        s = SystemStatus()
        s.timestamp = entry['timestamp']
        s.os_type = entry['os_type']
        s.os_version = entry['os_version']
        s.uptime = entry['uptime']
        s.idletime = entry['idletime']
        s.cpu_total = entry['cpu_total']
        s.memory_total = entry['memory_total']
        s.memory_free = entry['memory_free']
        s.swap_total = entry['swap_total']
        s.swap_free = entry['swap_free']

        for cu in entry['cpu_usages']:
            s.cpu_usages.append(cu)
        
        for be in entry['blockdevs']:
            b = BlockDevice()
            b.devicename = be['device']
            b.read = be['read']
            b.write = be['write']
            s.blockdevs.append(b)

        for pe in entry['processes']:
            p = RuntimeProcess()
            p.pid = pe['pid']
            p.name = pe['name']
            p.state = pe['state']
            p.utime = pe['utime']
            p.stime = pe['stime']
            p.memory = pe['memory']
            s.processes.append(p)
        
        for ne in entry['netdevs']:
            n = NetworkDevice()
            n.device = ne['device']
            n.send = ne['send']
            n.receive = ne['receive']
            s.netdevs.append(n)
            
        result.append(s)

    bdb.close()

    return result

def save_system_status(system_status):
    bdb = BSONBDB()

    today = datetime.date.today()
    log_file = SENTINELD_LOG_DIR + '/' + str(today.year) + str(today.month) + str(today.day) + '.db'
    
    bdb.open(log_file, BDBOWRITER | BDBOCREAT)
    bdb[str(system_status.timestamp)] = system_status.to_dict()

    bdb.close()
