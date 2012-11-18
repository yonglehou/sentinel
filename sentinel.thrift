#!/usr/local/bin/thrift --gen cpp

namespace php sentinel
namespace py sentinel
namespace rb sentinel

struct NetworkDeviceInfo {
       1: string device
       2: i64 send
       3: i64 receive
}

struct ProcessInfo {
       1: i32 pid
       2: string name
       3: string state
       4: i64 utime
       5: i64 stime
       6: i64 memory
}

struct MachineStatus {
       1: i64 timestamp
       2: string os_type
       3: string os_version
       4: i64 uptime
       5: i64 idletime
       6: i16 cpu_total
       7: list<i16> cpu_usages
       8: i64 memory_total
       9: i64 memory_free
       10: i64 swap_total
       11: i64 swap_free
       12: list<ProcessInfo> processes
       14: list<NetworkDeviceInfo> netdevs
}

struct CommandResponse {
       1: string message
}

service Sentinel {
	MachineStatus get_current_status(),
	list<i64> get_current_cpu_usages(),
	list<i64> get_current_memory_usages(),
	list<ProcessInfo> get_current_process_usages(),
	list<MachineStatus> report_machine_status(1: i64 from_date, 2: i64 to_date),
	CommandResponse do_system_command(1: string command),
}
