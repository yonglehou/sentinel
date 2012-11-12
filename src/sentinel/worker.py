from multiprocessing import Process
from datastore import SystemStatus, RuntimeProcess

import time
import datastore

monitor_attrs = ['system_version','uptime', 'load_average', 'cpu_status', 'memory_status', 'process_status']

class DataCollector:
    def __init__(self, system_status):
        self.system_status = system_status

    def __call__(self):
        datastore.initialize()
        datastore.save_system_status(self.system_status)
        print("Data Collector Called : %d" % self.system_status.timestamp)

class SystemMonitor:
    def __init__(self, platform_api):
        self.platform_api = platform_api

    def action(self):
        system_status = SystemStatus()
        for attr in monitor_attrs:
            if hasattr(self.platform_api, attr):
                api_func = getattr(self.platform_api, attr)
                api_func(system_status)

        return system_status

    def __call__(self):
        while(True):
            time.sleep(1)
            system_status = self.action()
            collectorp = Process(name='Sentinel Worker : DataCollector', target=DataCollector(system_status))
            collectorp.daemon = True
            collectorp.start()
