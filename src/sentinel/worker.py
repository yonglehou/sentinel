from multiprocessing import Process
from datastore import SystemStatus, RuntimeProcess

import time
import datastore

monitor_attrs = ['uptime', 'load_average', 'cpu_status', 'memory_status', 'process_status']

class DataCollector:
    def __init__(self, system_status):
        self.system_status = system_status

    def __call__(self):
        datastore.initialize()
        datastore.save_system_status(self.system_status)

class SystemMonitor:
    def __init__(self, platform_api):
        self.platform_api = platform_api

    def __call__(self):
        system_status = SystemStatus()
        if hasattr(self.platform_api, 'system_version'):
            api_func = getattr(self.platform_api, 'system_version')
            api_func(system_status)
        while(True):
            time.sleep(1)
            for attr in monitor_attrs:
                if hasattr(self.platform_api, attr):
                    api_func = getattr(self.platform_api, attr)
                    api_func(system_status)
            
            collectorp = Process(name='Sentinel Worker : DataCollector', target=DataCollector(system_status))
            collectorp.daemon = True
            collectorp.start()
