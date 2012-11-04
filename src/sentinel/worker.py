import time

monitor_attrs = ['uptime', 'load_average', 'cpu_status']

class SystemStatus:
    def __init__(self):
        self.os_type = ''
        self.os_version = ''
        self.uptime = 0
        self.idletime = 0
        self.cpu_total = None
        self.cpu_usages = []

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
            print(system_status.cpu_total)
            print(system_status.cpu_usages)
