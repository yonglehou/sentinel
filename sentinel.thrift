#!/usr/local/bin/thrift --gen cpp

namespace php sentinel
namespace py sentinel
namespace rb sentinel

struct MachineStatus {
       1: string info
}

struct CommandResponse {
       1: string message
}

service Sentinel {
	list<MachineStatus> report_machine_status(),
	CommandResponse do_system_command(1: string command),
}
