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
    def __init__(self, user, nice, system, idle):
        global hz
        self.user = user
        self.nice = nice
        self.system = system
        self.idle = idle

    def __str__(self):
        return "%ld %ld %ld %ld" % (self.user, self.nice, self.system, self.idle)

def delta_cpu(before_cpu, after_cpu):
    user_delta = after_cpu.user - before_cpu.user
    nice_delta = after_cpu.nice - before_cpu.nice
    system_delta = after_cpu.system - before_cpu.system
    idle_delta = after_cpu.idle - before_cpu.idle
    return LinuxCPU(user_delta, nice_delta, system_delta, idle_delta)

def get_cpu_usage(delta):
    total = delta.user + delta.nice + delta.system + delta.idle
    if total == 0:
        return 0
    return 100.0 * (total - delta.idle) / total

before_cpu_t = None
after_cpu_t = None
def get_cpu_t_delta(line):
    global before_cpu_t, after_cpu_t

    data = line.split(' ')
    cpu_t = LinuxCPU(long(data[2]), long(data[3]), long(data[4]), long(data[5]))
    if before_cpu_t == None:
        before_cpu_t = cpu_t
    else:
        before_cpu_t = after_cpu_t
    after_cpu_t = cpu_t

    return delta_cpu(before_cpu_t, after_cpu_t)

cpu_regex = re.compile(r'^cpu[0-9]+')    
before_cpu_n = None
after_cpu_n = None
def cpu_status(system_status):
    global before_cpu_n, after_cpu_n

    with open(PROC_STAT_FILE, 'r') as f:
        line = f.readline()
        delta_cpu_t = get_cpu_t_delta(line)
        cpu_n = []
        for line in f.readlines():
            if cpu_regex.match(line):
                data = line.split(' ')
                cpu = LinuxCPU(long(data[1]), long(data[2]), long(data[3]), long(data[4]))
                cpu_n.append(cpu)

        if before_cpu_n == None:
            before_cpu_n = cpu_n
        else:
            before_cpu_n = after_cpu_n

        after_cpu_n = cpu_n
        
        delta_cpu_n = []
        for i in range(len(after_cpu_n)):
            delta_cpu_n.append(delta_cpu(before_cpu_n[i], after_cpu_n[i]))

        system_status.cpu_total = get_cpu_usage(delta_cpu_t)
        system_status.cpu_usages = []
        for delta in delta_cpu_n:
            system_status.cpu_usages.append(get_cpu_usage(delta))

mem_total_regex = re.compile(r'MemTotal:')
mem_free_regex = re.compile(r'MemFree:')
swap_total_regex = re.compile(r'SwapTotal:')
swap_free_regex = re.compile(r'SwapFree:')
def memory_status(system_status):
    with open(PROC_MEMINFO_FILE, 'r') as f:
        for line in f.readlines():
            if mem_total_regex.match(line):
                data = line.split(' ')
                system_status.memory_total = data[len(data) - 2]
            elif mem_free_regex.match(line):
                data = line.split(' ')
                system_status.memory_free = data[len(data) - 2]
            elif swap_total_regex.match(line):
                data = line.split(' ')
                system_status.swap_total = data[len(data) - 2]
            elif swap_free_regex.match(line):
                data = line.split(' ')
                system_status.swap_free = data[len(data) - 2]

def proc_status(system_status):
    pass
