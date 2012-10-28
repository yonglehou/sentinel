import time

class SystemMonitor:
    def __init__(self, platform_api):
        self.platform_api = platform_api

    def __call__(self):
        while(True):
            time.sleep(1)
            if hasattr(self.platform_api, 'cpu_status'):
                self.platform_api.cpu_status()
            if hasattr(self.platform_api, 'version'):
                self.platform_api.version()
