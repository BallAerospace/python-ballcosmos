import os
import sys
import time
import threading

try:
    os.environ["COSMOS_VERSION"]
except KeyError:
    os.environ["COSMOS_VERSION"] = "5"

from ballcosmos.script import *

set_replay_mode(False)


def run_thread():
    print("Running thread")
    print(cmd("INST ABORT"))
    print(cmd_no_range_check("INST COLLECT with TYPE NORMAL, TEMP 50.0"))
    print(cmd_no_hazardous_check("INST CLEAR"))
    print(cmd_no_checks("INST COLLECT with TYPE SPECIAL, TEMP 50.0"))
    print(cmd_raw("INST COLLECT with TYPE 0, TEMP 10.0"))
    print(cmd_raw_no_range_check("INST COLLECT with TYPE 0, TEMP 50.0"))
    print(cmd_raw_no_hazardous_check("INST CLEAR"))
    print(cmd_raw_no_checks("INST COLLECT with TYPE 1, TEMP 50.0"))
    print("Thread completed")


thread = threading.Thread(target=run_thread)
thread.start()
thread.join()

print(connect_interface("EXAMPLE_INT"))
print(interface_state("TEMPLATED_INT"))

# ~ # telemetry.py
print(tlm("INST HEALTH_STATUS TEMP1"))
print(tlm_raw("INST HEALTH_STATUS TEMP1"))
print(tlm_formatted("INST HEALTH_STATUS TEMP1"))
print(tlm_with_units("INST HEALTH_STATUS TEMP1"))
print(tlm_variable("INST HEALTH_STATUS TEMP1", "RAW"))
print(set_tlm("INST HEALTH_STATUS TEMP1 = 5"))
print(set_tlm_raw("INST HEALTH_STATUS TEMP1 = 5"))
print(get_tlm_packet("INST", "HEALTH_STATUS"))
print(
    get_tlm_values(
        [["INST", "HEALTH_STATUS", "TEMP1"], ["INST", "HEALTH_STATUS", "TEMP2"]]
    )
)
print(get_tlm_list("INST"))
print(get_tlm_item_list("INST", "HEALTH_STATUS"))
print(get_target_list())
print(
    get_tlm_details(
        [["INST", "HEALTH_STATUS", "TEMP1"], ["INST", "HEALTH_STATUS", "TEMP2"]]
    )
)
print(get_tlm_buffer("INST", "HEALTH_STATUS"))
id = subscribe_packet_data([["INST", "HEALTH_STATUS"]])
print(get_packet_data(id))
unsubscribe_packet_data(id)

# commands.py
print(cmd("INST ABORT"))
print(cmd_no_range_check("INST COLLECT with TYPE NORMAL, TEMP 50.0"))
print(cmd_no_hazardous_check("INST CLEAR"))
print(cmd_no_checks("INST COLLECT with TYPE SPECIAL, TEMP 50.0"))
print(cmd_raw("INST COLLECT with TYPE 0, TEMP 10.0"))
print(cmd_raw_no_range_check("INST COLLECT with TYPE 0, TEMP 50.0"))
print(cmd_raw_no_hazardous_check("INST CLEAR"))
print(cmd_raw_no_checks("INST COLLECT with TYPE 1, TEMP 50.0"))
print(send_raw("EXAMPLE_INT", "\x00\x00\x00\x00"))
print(send_raw_file("EXAMPLE_INT", "C:\git\COSMOS\README.md"))
print(get_cmd_list("INST"))
print(get_cmd_param_list("INST", "COLLECT"))
print(get_cmd_hazardous("INST", "CLEAR"))
print(get_cmd_value("INST", "COLLECT", "TEMP"))
print(get_cmd_time())
print(get_cmd_buffer("INST", "COLLECT"))
print(cmd_no_range_check("INST COLLECT with TYPE NORMAL, TEMP 50.0"))

script_disconnect()

shutdown_cmd_tlm()
