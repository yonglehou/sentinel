from thrift.ttypes import *
from datetime import date, datetime, timedelta

import datastore

def translate_to_thrift_object(loaded):
    translated = []
    for s in loaded:
        ms = MachineStatus()
        ms.timestamp = s.timestamp
        ms.os_type = s.os_type
        ms.os_version = s.os_version
        ms.uptime = long(s.uptime)
        ms.idletime = long(s.idletime)
        ms.cpu_total = s.cpu_total
        ms.cpu_usages = s.cpu_usages
        ms.memory_total = s.memory_total
        ms.memory_free = s.memory_free
        ms.swap_total = s.swap_total
        ms.swap_free = s.swap_free
        ms.processes = []
        for p in s.processes:
            pi = ProcessInfo(p)
            pi.pid = p.pid
            pi.name = p.name
            pi.state = p.state
            pi.utime = long(p.utime)
            pi.stime = long(p.stime)
            pi.memory = p.memory
            ms.processes.append(pi)

        translated.append(ms)
    
    return translated

class SentinelHandler:
    def __init__(self):
        self.log = {}

    def report_machine_status(self, from_date, to_date):
        def datetime_iterator(from_date, to_date):
            while to_date is None or from_date <= to_date:
                yield from_date
                from_date = from_date + timedelta(days = 1)
            return
        
        from_date = date.fromtimestamp(from_date)
        to_date = date.fromtimestamp(to_date)
        
        status = []
        for d in datetime_iterator(from_date, to_date):
            try:
                loaded = datastore.load_system_status(d)
                status = status + translate_to_thrift_object(loaded)
            except Exception, e:
                print('Error: %s' % e)

        return status
    
    def do_system_command(self, command):
        cr = CommandResponse()
        cr.message = "Hello World"
        return cr
