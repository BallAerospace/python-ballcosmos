from ballcosmos.script.script import *

def tlm(*args):
  """Poll for the converted value of a telemetry item
  Usage:
    tlm(target_name, packet_name, item_name)
  or
    tlm('target_name packet_name item_name')
  """
  return cmd_tlm_server.write('tlm', *args)

def tlm_raw(*args):
  """Poll for the raw value of a telemetry item
  Usage:
    tlm_raw(target_name, packet_name, item_name)
  or
    tlm_raw('target_name packet_name item_name')
  """
  return cmd_tlm_server.write('tlm_raw', *args)

def tlm_formatted(*args):
  """Poll for the formatted value of a telemetry item
  Usage:
    tlm_formatted(target_name, packet_name, item_name)
  or
    tlm_formatted('target_name packet_name item_name')
  """
  return cmd_tlm_server.write('tlm_formatted', *args)

def tlm_with_units(*args):
  """Poll for the formatted with units value of a telemetry item
  Usage:
    tlm_with_units(target_name, packet_name, item_name)
  or
    tlm_with_units('target_name packet_name item_name')
  """
  return cmd_tlm_server.write('tlm_with_units', *args)

def tlm_variable(*args):
  return cmd_tlm_server.write('tlm_variable', *args)

def set_tlm(*args):
  """Set a telemetry point to a given value. Note this will be over written in
  a live system by incoming new telemetry.
  Usage:
    set_tlm(target_name, packet_name, item_name, value)
  or
    set_tlm("target_name packet_name item_name = value")
  """
  return cmd_tlm_server.write('set_tlm', *args)

def set_tlm_raw(*args):
  """Set the raw value of a telemetry point to a given value. Note this will
  be over written in a live system by incoming new telemetry.
  Usage:
    set_tlm_raw(target_name, packet_name, item_name, value)
  or
    set_tlm_raw("target_name packet_name item_name = value")
  """
  return cmd_tlm_server.write('set_tlm_raw', *args)

def override_tlm(*args):
  """Permanently set the converted value of a telemetry point to a given value
  Usage:
    override_tlm(target_name, packet_name, item_name, value)
  or
    override_tlm("target_name packet_name item_name = value")
  """
  return cmd_tlm_server.write('override_tlm', *args)

def override_tlm_raw(*args):
  """Permanently set the raw value of a telemetry point to a given value
  Usage:
    override_tlm_raw(target_name, packet_name, item_name, value)
  or
    override_tlm_raw("target_name packet_name item_name = value")
  """
  return cmd_tlm_server.write('override_tlm_raw', *args)

def normalize_tlm(*args):
  """Clear an override of a telemetry point
  Usage:
    normalize_tlm(target_name, packet_name, item_name)
  or
    normalize_tlm("target_name packet_name item_name")
  """
  return cmd_tlm_server.write('normalize_tlm', *args)

def get_tlm_packet(target_name, packet_name, value_types = "CONVERTED"):
  """Gets all the values from the given packet returned in a two dimensional
  array containing the item_name, value, and limits state.
  Usage:
    values = get_tlm_packet(target_name, packet_name, <:RAW, :CONVERTED, :FORMATTED, :WITH_UNITS>)
  """
  return cmd_tlm_server.write('get_tlm_packet', target_name, packet_name, value_types)

def get_tlm_values(items, value_types = "CONVERTED"):
  """Gets all the values from the given packet returned in an
  array consisting of an Array of item values, an array of item limits state
  given as symbols such as :RED, :YELLOW, :STALE, an array of arrays including
  the limits setting such as red low, yellow low, yellow high, red high and
  optionally green low and high, and the overall limits state of the system.
  Usage:
    values = get_tlm_values([[target_name, packet_name, item_name], ...], <:RAW, :CONVERTED, :FORMATTED, :WITH_UNITS>)
  """
  return cmd_tlm_server.write('get_tlm_values', items, value_types)

def get_tlm_list(target_name):
  """Gets the packets for a given target name. Returns an array of arrays
  consisting of packet names and packet descriptions.
  """
  return cmd_tlm_server.write('get_tlm_list', target_name)

def get_tlm_item_list(target_name, packet_name):
  """Gets all the telemetry mnemonics for a given target and packet. Returns an
  array of arrays consisting of item names, item states, and item descriptions"""
  return cmd_tlm_server.write('get_tlm_item_list', target_name, packet_name)

def get_target_list():
  """Gets the list of all defined targets."""
  return cmd_tlm_server.write('get_target_list')

def get_tlm_details(items):
  return cmd_tlm_server.write('get_tlm_details', items)

def get_tlm_buffer(target_name, packet_name):
  """Returns the buffer from the telemetry packet."""
  return cmd_tlm_server.write('get_tlm_buffer', target_name, packet_name)

def subscribe_packet_data(packets, queue_size = 1000):
  """Subscribe to one or more telemetry packets. The queue ID is returned for
  use in get_packet_data and unsubscribe_packet_data.
  Usage:
    id = subscribe_packet_data([[target_name,packet_name], ...], <queue_size>)
  """
  return cmd_tlm_server.write('subscribe_packet_data', packets, queue_size)

def unsubscribe_packet_data(id):
  """Unsubscribe to telemetry packets. Pass the queue ID which was returned by
  the subscribe_packet_data method.
  Usage:
    unsubscribe_packet_data(id)
  """
  return cmd_tlm_server.write('unsubscribe_packet_data', id)

def get_packet_data(id, non_block = False):
  """DEPRECATED - Currently the only option on python until we have config file parsing though"""
  return cmd_tlm_server.write('get_packet_data', id, non_block)

#~ # Get a packet which was previously subscribed to by
#~ # subscribe_packet_data. This method can block waiting for new packets or
#~ # not based on the second parameter. It returns a single Cosmos::Packet instance
#~ # and will return nil when no more packets are buffered (assuming non_block
#~ # is false).
#~ # Usage:
#~ #   get_packet(id, <true or false to block>)
#~ def get_packet(id, non_block = false)
  #~ packet = nil
  #~ buffer, target_name, packet_name, received_time, received_count = get_packet_data(id, non_block)
  #~ if buffer
    #~ packet = System.telemetry.packet(target_name, packet_name).clone
    #~ packet.buffer = buffer
    #~ packet.received_time = received_time
    #~ packet.received_count = received_count
  #~ end
  #~ packet
