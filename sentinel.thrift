#!/usr/local/bin/thrift --gen cpp

namespace php sentinel
namespace py sentinel
namespace rb sentinel

struct BlockDeviceInfo {
       1: string device
       2: i64 data_read
       3: i64 data_write
}

struct NetworkDeviceInfo {
       1: string device
       2: i64 data_send
       3: i64 data_receive
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
       6: list<double> loadavgs
       7: i16 cpu_total
       8: list<i16> cpu_usages
       9: i64 memory_total
       10: i64 memory_free
       11: i64 swap_total
       12: i64 swap_free
       13: list<ProcessInfo> processes
       14: list<NetworkDeviceInfo> netdevs
       15: list<BlockDeviceInfo> blockdevs
}

struct CommandResponse {
       1: string message
}

service Sentinel {
	void heartbeat(),
	MachineStatus get_current_status(),
	list<i64> get_current_cpu_usages(),
	list<i64> get_current_memory_usages(),
	list<ProcessInfo> get_current_process_usages(),
	list<MachineStatus> report_machine_status(1: i64 from_date, 2: i64 to_date),
	CommandResponse do_system_command(1: string command),
}
