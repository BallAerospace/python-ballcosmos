from ballcosmos.script.script import *

def get_out_of_limits():
  return cmd_tlm_server.write('get_out_of_limits')

def get_overall_limits_state(ignored_items = None):
  return cmd_tlm_server.write('get_overall_limits_state', ignored_items)

def limits_enabled(*args):
  return cmd_tlm_server.write('limits_enabled?', *args)

def enable_limits(*args):
  return cmd_tlm_server.write('enable_limits', *args)

def disable_limits(*args):
  return cmd_tlm_server.write('disable_limits', *args)

def get_stale(with_limits_only = False, target_name = None):
  return cmd_tlm_server.write('get_stale', with_limits_only, target_name)

def get_limits(target_name, packet_name, item_name, limits_set = None):
  return cmd_tlm_server.write('get_limits', target_name, packet_name, item_name, limits_set)

def set_limits(target_name, packet_name, item_name, red_low, yellow_low, yellow_high, red_high, green_low = None, green_high = None, limits_set = 'CUSTOM', persistence = None, enabled = True):
  return cmd_tlm_server.write('set_limits', target_name, packet_name, item_name, red_low, yellow_low, yellow_high, red_high, green_low, green_high, limits_set, persistence, enabled)

def get_limits_groups():
  return cmd_tlm_server.write('get_limits_groups')

def enable_limits_group(group_name):
  return cmd_tlm_server.write('enable_limits_group', group_name)

def disable_limits_group(group_name):
  return cmd_tlm_server.write('disable_limits_group', group_name)

def get_limits_sets():
  return cmd_tlm_server.write('get_limits_sets')

def set_limits_set(limits_set):
  return cmd_tlm_server.write('set_limits_set', limits_set)

def get_limits_set():
  return cmd_tlm_server.write('get_limits_set')

def subscribe_limits_events(queue_size = 1000):
  return cmd_tlm_server.write('subscribe_limits_events', queue_size)

def unsubscribe_limits_events(id):
  return cmd_tlm_server.write('unsubscribe_limits_events', id)

def get_limits_event(id, non_block = False):
  return cmd_tlm_server.write('get_limits_event', id, non_block)
