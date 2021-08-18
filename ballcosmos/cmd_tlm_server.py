#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
cmd_tlm_server.py
"""

# Copyright 2021 Ball Aerospace & Technologies Corp.
# All Rights Reserved.
#
# This program is free software; you can modify and/or redistribute it
# under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; version 3 with
# attribution addendums as found in the LICENSE.txt


import ballcosmos

DEFAULT_SERVER_MESSAGES_QUEUE_SIZE = 1000


def get_interface_targets(interface_name):
    return ballcosmos.CTS.write("get_interface_targets", interface_name)


def get_interface_names():
    return ballcosmos.CTS.write("get_interface_names")


def connect_interface(interface_name, *params):
    return ballcosmos.CTS.write("connect_interface", interface_name, *params)


def disconnect_interface(interface_name):
    return ballcosmos.CTS.write("disconnect_interface", interface_name)


def interface_state(interface_name):
    return ballcosmos.CTS.write("interface_state", interface_name)


def map_target_to_interface(target_name, interface_name):
    return ballcosmos.CTS.write("map_target_to_interface", target_name, interface_name)


def get_router_names():
    return ballcosmos.CTS.write("get_router_names")


def connect_router(router_name, *params):
    return ballcosmos.CTS.write("connect_router", router_name, *params)


def disconnect_router(router_name):
    return ballcosmos.CTS.write("disconnect_router", router_name)


def router_state(router_name):
    return ballcosmos.CTS.write("router_state", router_name)


def get_target_info(target_name):
    return ballcosmos.CTS.write("get_target_info", target_name)


def get_all_target_info():
    return ballcosmos.CTS.write("get_all_target_info")


def get_target_ignored_parameters(target_name):
    return ballcosmos.CTS.write("get_target_ignored_parameters", target_name)


def get_target_ignored_items(target_name):
    return ballcosmos.CTS.write("get_target_ignored_items", target_name)


def get_interface_info(interface_name):
    return ballcosmos.CTS.write("get_interface_info", interface_name)


def get_all_router_info():
    return ballcosmos.CTS.write("get_all_router_info")


def get_all_interface_info():
    return ballcosmos.CTS.write("get_all_interface_info")


def get_router_info(router_name):
    return ballcosmos.CTS.write("get_router_info", router_name)


def get_all_cmd_info():
    return ballcosmos.CTS.write("get_all_cmd_info")


def get_all_tlm_info():
    return ballcosmos.CTS.write("get_all_tlm_info")


def get_cmd_cnt(target_name, command_name):
    return ballcosmos.CTS.write("get_cmd_cnt", target_name, command_name)


def get_tlm_cnt(target_name, packet_name):
    return ballcosmos.CTS.write("get_tlm_cnt", target_name, packet_name)


def get_packet_loggers():
    return ballcosmos.CTS.write("get_packet_loggers")


def get_packet_logger_info(packet_logger_name):
    return ballcosmos.CTS.write("get_packet_logger_info", packet_logger_name)


def get_all_packet_logger_info():
    return ballcosmos.CTS.write("get_all_packet_logger_info")


def get_background_tasks():
    return ballcosmos.CTS.write("get_background_tasks")


def start_background_task(task_name):
    return ballcosmos.CTS.write("start_background_task", task_name)


def stop_background_task(task_name):
    return ballcosmos.CTS.write("stop_background_task", task_name)


def get_server_status():
    return ballcosmos.CTS.write("get_server_status")


def get_cmd_log_filename(packet_log_writer_name="DEFAULT"):
    return ballcosmos.CTS.write("get_cmd_log_filename", packet_log_writer_name)


def get_tlm_log_filename(packet_log_writer_name="DEFAULT"):
    return ballcosmos.CTS.write("get_tlm_log_filename", packet_log_writer_name)


def start_logging(packet_log_writer_name="ALL", label=None):
    return ballcosmos.CTS.write("start_logging", packet_log_writer_name, label)


def stop_logging(packet_log_writer_name="ALL"):
    return ballcosmos.CTS.write("stop_logging", packet_log_writer_name)


def start_cmd_log(packet_log_writer_name="ALL", label=None):
    return ballcosmos.CTS.write("start_cmd_log", packet_log_writer_name, label)


def start_tlm_log(packet_log_writer_name="ALL", label=None):
    return ballcosmos.CTS.write("start_tlm_log", packet_log_writer_name, label)


def stop_cmd_log(packet_log_writer_name="ALL"):
    return ballcosmos.CTS.write("stop_cmd_log", packet_log_writer_name)


def stop_tlm_log(packet_log_writer_name="ALL"):
    return ballcosmos.CTS.write("stop_tlm_log", packet_log_writer_name)


def start_raw_logging_interface(interface_name="ALL"):
    return ballcosmos.CTS.write("start_raw_logging_interface", interface_name)


def stop_raw_logging_interface(interface_name="ALL"):
    return ballcosmos.CTS.write("stop_raw_logging_interface", interface_name)


def start_raw_logging_router(router_name="ALL"):
    return ballcosmos.CTS.write("start_raw_logging_router", router_name)


def stop_raw_logging_router(router_name="ALL"):
    return ballcosmos.CTS.write("stop_raw_logging_router", router_name)


def get_server_message_log_filename():
    return ballcosmos.CTS.write("get_server_message_log_filename")


def start_new_server_message_log():
    return ballcosmos.CTS.write("start_new_server_message_log")


def subscribe_server_messages(queue_size=DEFAULT_SERVER_MESSAGES_QUEUE_SIZE):
    return ballcosmos.CTS.write("subscribe_server_messages", queue_size)


def unsubscribe_server_messages(id_):
    return ballcosmos.CTS.write("unsubscribe_server_messages", id_)


def get_server_message(id_, non_block=False):
    return ballcosmos.CTS.write("get_server_message", id_, non_block)


def cmd_tlm_reload():
    return ballcosmos.CTS.write("cmd_tlm_reload")


def cmd_tlm_clear_counters():
    return ballcosmos.CTS.write("cmd_tlm_clear_counters")


def get_output_logs_filenames(filter="*tlm.bin"):
    return ballcosmos.CTS.write("get_output_logs_filenames", filter)
