from thrift.ttypes import *
from datetime import date, datetime, timedelta
from worker import SystemMonitor
from datastore import SystemStatus

import datastore

def runtime_process_translate_to_thrift_object(p):
    pi = ProcessInfo()
    pi.pid = p.pid
    pi.name = p.name
    pi.state = p.state
    pi.utime = p.utime
    pi.stime = p.stime
    pi.memory = p.memory
    return pi

def network_device_translate_to_thrift_object(n):
    ni = NetworkDeviceInfo()
    ni.device = n.device
    ni.send = n.send
    ni.receive = n.receive
    return ni

def block_device_translate_to_thrift_object(b):
    bi = BlockDeviceInfo()
    bi.device = b.device
    bi.read = b.read
    bi.write = b.write
    return bi

def system_status_translate_to_thrift_object(s):
    ms = MachineStatus()
    ms.timestamp = s.timestamp
    ms.os_type = s.os_type
    ms.os_version = s.os_version
    ms.uptime = s.uptime
    ms.idletime = s.idletime
    ms.cpu_total = s.cpu_total
    ms.cpu_usages = s.cpu_usages
    ms.memory_total = s.memory_total
    ms.memory_free = s.memory_free
    ms.swap_total = s.swap_total
    ms.swap_free = s.swap_free
    ms.processes = []
    ms.netdevs = []
    for p in s.processes:
        pi = runtime_process_translate_to_thrift_object(p)
        ms.processes.append(pi)
    for n in s.netdevs:
        ni = network_device_translate_to_thrift_object(n)
        ms.netdevs.append(ni)
    for b in s.blockdevs:
        bi = block_device_translate_to_thrift_object(b)
        ms.blockdevs.append(bi)

    return ms

class SentinelHandler:
    def __init__(self, platform_api):
        self.platform_api = platform_api;
        
    def get_current_status(self):
        system_status = SystemMonitor(self.platform_api).action()

        return system_status_translate_to_thrift_object(system_status)

    def get_current_cpu_usages(self):
        system_status = SystemStatus()
        self.platform_api.cpu_status(system_status)
        l = [system_status.timestamp, system_status.cpu_total]
        l = l + system_status.cpu_usages
        return l

    def get_current_memory_usages(self):
        system_status = SystemStatus()
        self.platform_api.memory_status(system_status)
        return [system_status.timestamp, system_status.memory_total, system_status.memory_free, system_status.swap_total, system_status.swap_free]

    def get_current_process_usages(self):
        system_status = SystemStatus()
        self.platform_api.process_status(system_status)
        pl = []
        for p in system_status.processes:
            pi = runtime_process_translate_to_thrift_object(p)
            pl.append(pi)
        return pl

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
                translated = []
                for s in loaded:
                    translated.append(system_status_translated_to_thrift_object(s))
                status = status + translated
            except Exception, e:
                print('Error: %s' % e)

        return status
    
    def do_system_command(self, command):
        cr = CommandResponse()
        cr.message = "Hello World"
        return cr
