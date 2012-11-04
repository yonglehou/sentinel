import time

monitor_attrs = ['uptime', 'load_average', 'cpu_status', 'memory_status', 'process_status']

class SystemStatus:
    def __init__(self):
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
            
