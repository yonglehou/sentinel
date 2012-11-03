import re

PROC_CPUINFO_FILE = '/proc/cpuinfo'
PROC_MEMINFO_FILE = '/proc/meminfo'
PROC_STAT_FILE = '/proc/stat'
PROC_SWAPS_FILE = '/proc/swaps'
PROC_DISKSTATS_FILE = '/proc/diskstats'
PROC_PARTITIONS_FILE = '/proc/partitions'
PROC_UPTIME_FILE = '/proc/uptime'
PROC_MDSTAT_FILE = '/proc/mdstat'
PROC_LOADAVG_FILE = '/proc/loadavg'
PROC_VERSION_FILE = '/proc/version'

cpu_regex = re.compile(r'^cpu[0-9]+')

def system_version(system_status):
    with open(PROC_VERSION_FILE, 'r') as f:
        line = f.readline()
        data = line.split(' ')
        system_status.os_type, system_status.os_version = data[0], data[1]

def load_average(system_status):
    with open(PROC_LOADAVG_FILE, 'r') as f:
        line = f.readline()
        data = line.split(' ')
        system_status.loadavg1, system_status.loadavg5, system_status.loadavg15 = data[0], data[1], data[2]

def uptime(system_status):
    with open(PROC_UPTIME_FILE, 'r') as f:
        line = f.readline()
        data = line.split(' ')
        system_status.uptime, system_status.idletime = data[0], data[1]

class LinuxCPU:
    def __init__(self, user, nice, system, idle, iowait, irq, softirq):
        self.user = user
        self.nice = nice
        self.system = system
        self.idle = idle
        self.iowait = iowait
        self.irq = irq
        self.softirq = softirq

    def __str__(self):
        return "%d %d %d %d %d %d %d" % (self.user, self.nice, self.system, self.idle, self.iowait, self.irq, self.softirq)

def get_cpu_status(line):
    data = line.split(' ')
    cpu = LinuxCPU(int(data[2]), int(data[3]), int(data[4]), int(data[5]), int(data[6]), int(data[7]), int(data[8]))
    return 100 * cpu.idle / (cpu.user + cpu.nice + cpu.system + cpu.idle)

def get_cpun_status(line):
    data = line.split(' ')
    cpu = LinuxCPU(int(data[1]), int(data[2]), int(data[3]), int(data[4]), int(data[5]), int(data[6]), int(data[7]))
    return 100 * cpu.idle / (cpu.user + cpu.nice + cpu.system + cpu.idle)

def cpu_status(system_status):
    with open(PROC_STAT_FILE, 'r') as f:
        line = f.readline()
        system_status.cpu_total = get_cpu_status(line)
        system_status.cpu_usages = []
        for line in f.readlines():
            if cpu_regex.match(line):
                system_status.cpu_usages.append(get_cpun_status(line))
