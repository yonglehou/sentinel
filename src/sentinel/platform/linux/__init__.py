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

def cpu_status():
    pass

def uptime():
    pass

def version():
    version_str = open(PROC_VERSION_FILE, 'r').read()
