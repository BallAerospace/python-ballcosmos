#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-

import threading
import os

# os.environ["COSMOS_LOG_LEVEL"] = "DEBUG"

from ballcosmos import *


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
id_ = subscribe_packet_data([["INST", "HEALTH_STATUS"]])
print(get_packet_data(id_))
unsubscribe_packet_data(id_)

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
FILE_PATH = os.path.dirname(os.path.abspath(__file__))
print(send_raw_file("EXAMPLE_INT", os.path.join(FILE_PATH, "test.txt")))
print(get_cmd_list("INST"))
print(get_cmd_param_list("INST", "COLLECT"))
print(get_cmd_hazardous("INST", "CLEAR"))
print(get_cmd_value("INST", "COLLECT", "TEMP"))
print(get_cmd_time())
print(get_cmd_buffer("INST", "COLLECT"))
print(cmd_no_range_check("INST COLLECT with TYPE NORMAL, TEMP 50.0"))

# tools.py
display("INST ADCS")
display("INST HS")
display("INST COMMANDING")
clear("INST ADCS")
clear_all()
print(get_screen_list())
print(get_screen_definition("INST ADCS"))

# limits.py
print(get_out_of_limits())
print(get_overall_limits_state())
print(limits_enabled("INST HEALTH_STATUS TEMP1"))
print(disable_limits("INST HEALTH_STATUS TEMP1"))
print(enable_limits("INST HEALTH_STATUS TEMP1"))
print(get_stale())
print(get_limits("INST", "HEALTH_STATUS", "TEMP1"))
print(set_limits("INST", "HEALTH_STATUS", "TEMP1", -50, -25, 25, 50))
print(get_limits_groups())
print(enable_limits_group("INST2_TEMP2"))
print(disable_limits_group("INST2_TEMP2"))
print(get_limits_sets())
print(set_limits_set("TVAC"))
print(get_limits_set())
print(set_limits_set("DEFAULT"))
id_ = subscribe_limits_events()
print(get_limits_event(id_))
print(unsubscribe_limits_events(id_))


# cmd_tlm_server.py
print(get_interface_names())
print(disconnect_interface("INST_INT"))
print(connect_interface("INST_INT"))
print(interface_state("INST_INT"))
print(map_target_to_interface("INST", "INST_INT"))
print(get_router_names())
print(connect_router("INST_ROUTER"))
print(disconnect_router("INST_ROUTER"))
print(router_state("INST_ROUTER"))
print(get_target_info("INST"))
print(get_all_target_info())
print(get_target_ignored_parameters("INST"))
print(get_target_ignored_items("INST"))
print(get_interface_info("INST_INT"))
print(get_all_router_info())
print(get_router_info("PREIDENTIFIED_ROUTER"))
print(get_all_interface_info())
print(get_all_cmd_info())
print(get_all_tlm_info())
print(get_cmd_cnt("INST", "COLLECT"))
print(get_tlm_cnt("INST", "ADCS"))
print(get_packet_loggers())
print(get_packet_logger_info("DEFAULT"))
print(get_all_packet_logger_info())
print(get_background_tasks())
print(stop_background_task("Limits Groups"))
print(start_background_task("Limits Groups"))
print(get_server_status())
print(get_cmd_log_filename())
print(get_tlm_log_filename())
print(stop_logging())
print(start_logging())
print(stop_cmd_log())
print(stop_tlm_log())
print(start_cmd_log())
print(start_tlm_log())
print(start_raw_logging_interface())
print(stop_raw_logging_interface())
print(start_raw_logging_router())
print(stop_raw_logging_router())
print(get_server_message_log_filename())
print(start_new_server_message_log())
id_ = subscribe_server_messages()
print(get_server_message(id_))
unsubscribe_server_messages(id_)
print(cmd_tlm_clear_counters())
print(get_output_logs_filenames())
print(cmd_tlm_reload())
print(connect_interface("EXAMPLE_INT"))
print(interface_state("TEMPLATED_INT"))


# scripting.py
try:
    print(play_wav_file("ding.wav"))
except NotImplementedError:
    pass

try:
    print(status_bar("hello"))
except NotImplementedError:
    pass

# api_shared.py
print(check("INST HEALTH_STATUS TEMP1 > -200"))
print(check_formatted("INST HEALTH_STATUS COLLECT_TYPE == 'NORMAL'"))
print(check_with_units("INST HEALTH_STATUS COLLECT_TYPE == 'NORMAL'"))
print(check_raw("INST HEALTH_STATUS COLLECT_TYPE == 0"))
print(check_tolerance("INST HEALTH_STATUS TEMP1", 0, -200.0))
print(check_tolerance_raw("INST HEALTH_STATUS TEMP1", 0, -200000.0))
print(check_expression("True == True"))
print(wait("INST HEALTH_STATUS TEMP1 > -200", 5))
print(wait_raw("INST HEALTH_STATUS COLLECT_TYPE == 0", 5))
print(wait_tolerance("INST HEALTH_STATUS TEMP1", 0, -200.0, 5))
print(wait_tolerance_raw("INST HEALTH_STATUS TEMP1", 0, -200000.0, 5))
print(wait_expression("True == True", 5))
print(wait_check("INST HEALTH_STATUS TEMP1 > -200", 5))
print(wait_check_raw("INST HEALTH_STATUS COLLECT_TYPE == 0", 5))
print(wait_check_tolerance("INST HEALTH_STATUS TEMP1", 0, -200.0, 5))
print(wait_check_tolerance_raw("INST HEALTH_STATUS TEMP1", 0, -200000.0, 5))
print(wait_check_expression("True == True", 5))
print(wait_check_expression("interface_state('TEMPLATED_INT') == 'DISCONNECTED'", 5))
print(wait_expression_stop_on_timeout("True == True", 5))
print(wait_packet("INST", "HEALTH_STATUS", 3, 5))
print(wait_check_packet("INST", "HEALTH_STATUS", 3, 5))

# replay.py
set_replay_mode(True)
filename = get_output_logs_filenames()[-1]
print(replay_select_file(filename))
print(replay_status())
print(replay_set_playback_delay(1))
print(replay_play())
print(replay_reverse_play())
print(replay_stop())
print(replay_step_forward())
print(replay_step_back())
print(replay_move_start())
print(replay_move_end())
print(replay_move_index(0))

set_replay_mode(False)

# scripting.py
print(ask_string("Question?:"))
print(ask("Well?:"))
print(prompt("Hit Ok"))
print(message_box("message here", "one", "two"))
print(vertical_message_box("message here", "one", "two"))
print(combo_box("message here", "one", "two"))
print(save_file_dialog())
print(open_file_dialog())
print(open_files_dialog())
print(open_directory_dialog())

thread = threading.Thread(target=run_thread)
thread.start()
thread.join()

disconnect()

shutdown()
