from sentinel.datastore import RuntimeProcess, BlockDevice, NetworkDevice
import os
import re

PROC_DIR = '/proc'
PROC_CPUINFO_FILE = PROC_DIR + '/cpuinfo'
PROC_MEMINFO_FILE = PROC_DIR + '/meminfo'
PROC_STAT_FILE = PROC_DIR + '/stat'
PROC_SWAPS_FILE = PROC_DIR + '/swaps'
PROC_DISKSTATS_FILE = PROC_DIR + '/diskstats'
PROC_PARTITIONS_FILE = PROC_DIR + '/partitions'
PROC_UPTIME_FILE = PROC_DIR + '/uptime'
PROC_MDSTAT_FILE = PROC_DIR + '/mdstat'
PROC_LOADAVG_FILE = PROC_DIR + '/loadavg'
PROC_VERSION_FILE = PROC_DIR + '/version'
PROC_NETSTAT_FILE = PROC_DIR + '/net/dev'

def system_version(system_status):
    with open(PROC_VERSION_FILE, 'r') as f:
        line = f.readline()
        data = line.split(' ')
        system_status.os_type, system_status.os_version = data[0], data[2]

def load_average(system_status):
    with open(PROC_LOADAVG_FILE, 'r') as f:
        line = f.readline()
        data = line.split(' ')
        system_status.loadavg1, system_status.loadavg5, system_status.loadavg15 = data[0], data[1], data[2]

def uptime(system_status):
    with open(PROC_UPTIME_FILE, 'r') as f:
        line = f.readline()
        data = line.split(' ')
        system_status.uptime, system_status.idletime = long(float(data[0])), long(float(data[1]))

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
                system_status.memory_total = long(data[len(data) - 2])
            elif mem_free_regex.match(line):
                data = line.split(' ')
                system_status.memory_free = long(data[len(data) - 2])
            elif swap_total_regex.match(line):
                data = line.split(' ')
                system_status.swap_total = long(data[len(data) - 2])
            elif swap_free_regex.match(line):
                data = line.split(' ')
                system_status.swap_free = long(data[len(data) - 2])

def disk_status(system_status):
    with open(PROC_DISKSTATS_FILE, 'r') as f:        
        pass

process_dir_regex = re.compile(r'[0-9]+')
PROC_PROCESS_STAT_PATTERN = PROC_DIR + '/%d/stat'
PROC_PROCESS_CMDLINE_PATTERN = PROC_DIR + '/%d/cmdline'
def process_status(system_status):
    def create_process_info(proc_stat_filename):
        process = RuntimeProcess()
        with open(proc_stat_filename, 'r') as f:
            data = f.read().split(' ')
            process.pid = long(data[0])
            process.name = data[1][1:-1]
            process.state = data[2]
            process.utime = long(data[13])
            process.stime = long(data[14])
            process.memory = long(data[22])
        return process

    processes = []
    proc_subdirs = os.listdir('/proc')
    for dentry in proc_subdirs:
        if process_dir_regex.match(dentry):
            try:
                proc_cmdline_filename = PROC_PROCESS_CMDLINE_PATTERN % long(dentry)
                if '' != open(proc_cmdline_filename).read():
                    proc_stat_filename = PROC_PROCESS_STAT_PATTERN % long(dentry)
                    proc_stat = create_process_info(proc_stat_filename)
                    processes.append(proc_stat)
            except:
                pass

    system_status.processes = processes

blockio_dev_regex = re.compile(r'')
def disk_status(system_status):
    with open(PROC_DISKSTATS_FILE, 'r') as f:
        system_status.blockdevs = []
        for line in f.readlines():
            if blockio_dev_regex.match(line):
                values = []
                for i in line.split(' '):
                    if i != '':
                        values.append(i)
                major_no = values[0]
                minor_no = values[1]
                if int(major_no) == 8:
                    device = values[2].strip(' \t\n\r')
                    read_complete = long(values[3])
                    write_complete = long(values[8])

                    blockd = BlockDevice()
                    blockd.read = read_complete
                    blockd.write = write_complete
                    
                    system_status.blockdevs.append(blockd)
                    

netstat_dev_regex = re.compile(r'.+:')
def network_status(system_status):
    with open(PROC_NETSTAT_FILE, 'r') as f:
        system_status.netdevs = []
        for line in f.readlines():
            if netstat_dev_regex.match(line):
                device, value_str = line.split(':')
                values = []
                for i in value_str.split(' '):
                    if i != '':
                        values.append(i)
                net_in = long(values[0])
                net_out = long(values[8])
                
                netdev = NetworkDevice()
                netdev.device = device.strip(' \t\n\r')
                netdev.receive = net_in
                netdev.send = net_out
                
                system_status.netdevs.append(netdev)

