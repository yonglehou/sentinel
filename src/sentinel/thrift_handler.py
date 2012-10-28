class ThriftHandler():
    def __init__(self):
        self.log = {}

    def report_machine_status(self):
        ms = MachineStatus()
        ms.info = "Machine Status"
        return [ms]
    
    def do_system_command(self, command):
        cr = CommandResponse()
        cr.message = "Hello World"
        return cr
