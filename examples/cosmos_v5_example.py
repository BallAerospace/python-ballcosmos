import os
import sys

# Updated from v0 to v1 for the ballcosmos libaray. In v1 the libary is
# expacting a version. If you are using cosmos v5 you do not need to set the
# environment variable `COSMOS_VERSION` to equal 5 it will default to use v5.
# If this is set the api endpoint and authentication will be correct.

try:
    os.environ["COSMOS_VERSION"]
except KeyError:
    os.environ["COSMOS_VERSION"] = "5"


# Updated from v0 to v1 for the ballcosmos libaray. In v1 the libary can log
# much more of what is happening in the libary. If you wish to enable this you
# MUST set the environment variable `COSMOS_DEBUG` to equal "DEBUG". If this 
# is not set you will not get log messages if this is an incorrect log level
# you will get a ValueError.

try:
    os.environ["COSMOS_DEBUG"]
except KeyError:
    os.environ["COSMOS_DEBUG"] = ""

# Updated from v0 to v1 for the ballcosmos libaray. In v1 you CAN set the hostname
# for all Cosmos v4 scripts. In v0 of ballcosmos it would default to 127.0.0.1.
# The hostname can now be set via an environment variable `COSMOS_HOSTNAME` to
# network address of the computer running Cosmos.

try:
    os.environ["COSMOS_HOSTNAME"]
except KeyError:
    os.environ["COSMOS_HOSTNAME"] = "127.0.0.1"


# Updated from v0 to v1 for the ballcosmos libaray. In v1 you MUST set the port
# for all cosmos v4 scripts. In v0 of ballcosmos the port was hard coded and
# would default to 7777 for Cosmos v4. In v1 the port can be set via an environment variable 
# `COSMOS_PORT` to the network port of the computer running Cosmos. Note the new
# port for Cosmos v5 is 2900

try:
    os.environ["COSMOS_PORT"]
except KeyError:
    os.environ["COSMOS_PORT"] = "2900"


from ballcosmos.script import *

set_replay_mode(False)

# ~ # telemetry.py
telemetry = [
    tlm("INST HEALTH_STATUS TEMP1"),
    tlm_raw("INST HEALTH_STATUS TEMP1"),
    tlm_formatted("INST HEALTH_STATUS TEMP1"),
    tlm_with_units("INST HEALTH_STATUS TEMP1"),
    tlm_variable("INST HEALTH_STATUS TEMP1", "RAW"),
    set_tlm("INST HEALTH_STATUS TEMP1 = 5"),
    set_tlm_raw("INST HEALTH_STATUS TEMP1 = 5"),
    get_tlm_packet("INST", "HEALTH_STATUS"),
    get_tlm_values(
        [["INST", "HEALTH_STATUS", "TEMP1"], ["INST", "HEALTH_STATUS", "TEMP2"]]
    ),
    get_tlm_list("INST"),
    get_tlm_item_list("INST", "HEALTH_STATUS"),
    get_target_list(),
    get_tlm_details(
        [["INST", "HEALTH_STATUS", "TEMP1"], ["INST", "HEALTH_STATUS", "TEMP2"]]
    ),
    get_tlm_buffer("INST", "HEALTH_STATUS"),
]
for i in telemetry:
    try:
        i.result
    except AttributeError:
        print(i)

id_ = subscribe_packet_data([["INST", "HEALTH_STATUS"]])
get_packet_data(id_)
unsubscribe_packet_data(id_)

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
# commands.py
commands = [
    cmd("INST ABORT"),
    cmd_no_range_check("INST COLLECT with TYPE NORMAL, TEMP 50.0"),
    cmd_no_hazardous_check("INST CLEAR"),
    cmd_no_checks("INST COLLECT with TYPE SPECIAL, TEMP 50.0"),
    cmd_raw("INST COLLECT with TYPE 0, TEMP 10.0"),
    cmd_raw_no_range_check("INST COLLECT with TYPE 0, TEMP 50.0"),
    cmd_raw_no_hazardous_check("INST CLEAR"),
    cmd_raw_no_checks("INST COLLECT with TYPE 1, TEMP 50.0"),
    send_raw("EXAMPLE_INT", "\x00\x00\x00\x00"),
    send_raw_file("EXAMPLE_INT", os.path.join(FILE_PATH, "test.txt")),
    get_cmd_list("INST"),
    get_cmd_param_list("INST", "COLLECT"),
    get_cmd_hazardous("INST", "CLEAR"),
    get_cmd_value("INST", "COLLECT", "TEMP"),
    get_cmd_time(),
    get_cmd_buffer("INST", "COLLECT"),
    cmd_no_range_check("INST COLLECT with TYPE NORMAL, TEMP 50.0"),
]
for i in commands:
    try:
        i.result
    except AttributeError:
        print(i)
        sys.exit(1)

update_scope("UPDATE")

script_disconnect()
shutdown_cmd_tlm()
