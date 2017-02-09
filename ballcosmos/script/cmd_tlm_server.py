from ballcosmos.script.script import *

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
