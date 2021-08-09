#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
cmd_tlm_server.py
"""

# Copyright 2017 Ball Aerospace & Technologies Corp.
# All Rights Reserved.
#
# This program is free software; you can modify and/or redistribute it
# under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; version 3 with
# attribution addendums as found in the LICENSE.txt


from ballcosmos import cmd_tlm_server

DEFAULT_SERVER_MESSAGES_QUEUE_SIZE = 1000

def get_interface_targets(interface_name):
  return cmd_tlm_server.write('get_interface_targets', interface_name)

def get_interface_names():
  return cmd_tlm_server.write('get_interface_names')

def connect_interface(interface_name, *params):
  return cmd_tlm_server.write('connect_interface', interface_name, *params)

def disconnect_interface(interface_name):
  return cmd_tlm_server.write('disconnect_interface', interface_name)

def interface_state(interface_name):
  return cmd_tlm_server.write('interface_state', interface_name)

def map_target_to_interface(target_name, interface_name):
  return cmd_tlm_server.write('map_target_to_interface', target_name, interface_name)

def get_router_names():
  return cmd_tlm_server.write('get_router_names')

def connect_router(router_name, *params):
  return cmd_tlm_server.write('connect_router', router_name, *params)

def disconnect_router(router_name):
  return cmd_tlm_server.write('disconnect_router', router_name)

def router_state(router_name):
  return cmd_tlm_server.write('router_state', router_name)

def get_target_info(target_name):
  return cmd_tlm_server.write('get_target_info', target_name)

def get_all_target_info():
  return cmd_tlm_server.write('get_all_target_info')

def get_target_ignored_parameters(target_name):
  return cmd_tlm_server.write('get_target_ignored_parameters', target_name)

def get_target_ignored_items(target_name):
  return cmd_tlm_server.write('get_target_ignored_items', target_name)

def get_interface_info(interface_name):
  return cmd_tlm_server.write('get_interface_info', interface_name)

def get_all_router_info():
  return cmd_tlm_server.write('get_all_router_info')

def get_all_interface_info():
  return cmd_tlm_server.write('get_all_interface_info')

def get_router_info(router_name):
  return cmd_tlm_server.write('get_router_info', router_name)

def get_all_cmd_info():
  return cmd_tlm_server.write('get_all_cmd_info')

def get_all_tlm_info():
  return cmd_tlm_server.write('get_all_tlm_info')

def get_cmd_cnt(target_name, command_name):
  return cmd_tlm_server.write('get_cmd_cnt', target_name, command_name)

def get_tlm_cnt(target_name, packet_name):
  return cmd_tlm_server.write('get_tlm_cnt', target_name, packet_name)

def get_packet_loggers():
  return cmd_tlm_server.write('get_packet_loggers')

def get_packet_logger_info(packet_logger_name):
  return cmd_tlm_server.write('get_packet_logger_info', packet_logger_name)

def get_all_packet_logger_info():
  return cmd_tlm_server.write('get_all_packet_logger_info')

def get_background_tasks():
  return cmd_tlm_server.write('get_background_tasks')

def start_background_task(task_name):
  return cmd_tlm_server.write('start_background_task', task_name)

def stop_background_task(task_name):
  return cmd_tlm_server.write('stop_background_task', task_name)

def get_server_status():
  return cmd_tlm_server.write('get_server_status')

def get_cmd_log_filename(packet_log_writer_name = 'DEFAULT'):
  return cmd_tlm_server.write('get_cmd_log_filename', packet_log_writer_name)

def get_tlm_log_filename(packet_log_writer_name = 'DEFAULT'):
  return cmd_tlm_server.write('get_tlm_log_filename', packet_log_writer_name)

def start_logging(packet_log_writer_name = 'ALL', label = None):
  return cmd_tlm_server.write('start_logging', packet_log_writer_name, label)

def stop_logging(packet_log_writer_name = 'ALL'):
  return cmd_tlm_server.write('stop_logging', packet_log_writer_name)

def start_cmd_log(packet_log_writer_name = 'ALL', label = None):
  return cmd_tlm_server.write('start_cmd_log', packet_log_writer_name, label)

def start_tlm_log(packet_log_writer_name = 'ALL', label = None):
  return cmd_tlm_server.write('start_tlm_log', packet_log_writer_name, label)

def stop_cmd_log(packet_log_writer_name = 'ALL'):
  return cmd_tlm_server.write('stop_cmd_log', packet_log_writer_name)

def stop_tlm_log(packet_log_writer_name = 'ALL'):
  return cmd_tlm_server.write('stop_tlm_log', packet_log_writer_name)

def start_raw_logging_interface(interface_name = 'ALL'):
  return cmd_tlm_server.write('start_raw_logging_interface', interface_name)

def stop_raw_logging_interface(interface_name = 'ALL'):
  return cmd_tlm_server.write('stop_raw_logging_interface', interface_name)

def start_raw_logging_router(router_name = 'ALL'):
  return cmd_tlm_server.write('start_raw_logging_router', router_name)

def stop_raw_logging_router(router_name = 'ALL'):
  return cmd_tlm_server.write('stop_raw_logging_router', router_name)

def get_server_message_log_filename():
  return cmd_tlm_server.write('get_server_message_log_filename')

def start_new_server_message_log():
  return cmd_tlm_server.write('start_new_server_message_log')

def subscribe_server_messages(queue_size = DEFAULT_SERVER_MESSAGES_QUEUE_SIZE):
  return cmd_tlm_server.write('subscribe_server_messages', queue_size)

def unsubscribe_server_messages(id):
  return cmd_tlm_server.write('unsubscribe_server_messages', id)

def get_server_message(id, non_block = False):
  return cmd_tlm_server.write('get_server_message', id, non_block)

def cmd_tlm_reload():
  return cmd_tlm_server.write('cmd_tlm_reload')

def cmd_tlm_clear_counters():
  return cmd_tlm_server.write('cmd_tlm_clear_counters')

def get_output_logs_filenames(filter = '*tlm.bin'):
  return cmd_tlm_server.write('get_output_logs_filenames', filter)
