import logging
from ballcosmos.script.script import *

def _log_cmd(target_name, cmd_name, cmd_params, raw, no_range, no_hazardous):
  """Log any warnings about disabling checks and log the command itself
  NOTE: This is a helper method and should not be called directly"""
  logger = logging.getLogger('ballcosmos')
  if no_range:
    logger.warning("Command #{target_name} #{cmd_name} being sent ignoring range checks")
  if no_hazardous:
    logger.warning("Command #{target_name} #{cmd_name} being sent ignoring hazardous warnings")
  logger.info(build_cmd_output_string(target_name, cmd_name, cmd_params, raw))
  return None

def _cmd(cmd, cmd_no_hazardous, *args):
  """Send the command and log the results
  NOTE: This is a helper method and should not be called directly"""
  raw = 'raw' in cmd
  no_range = 'no_range' in cmd or 'no_checks' in cmd
  no_hazardous = 'no_hazardous' in cmd or 'no_checks' in cmd

  while True:
    try:
      target_name, cmd_name, cmd_params = cmd_tlm_server.write(cmd, *args)
      _log_cmd(target_name, cmd_name, cmd_params, raw, no_range, no_hazardous)
    except HazardousError as e:
      ok_to_proceed = prompt_for_hazardous(e.target_name, e.cmd_name, e.hazardous_description)
      if ok_to_proceed:
        target_name, cmd_name, cmd_params = cmd_tlm_server.write(cmd_no_hazardous, *args)
        _log_cmd(target_name, cmd_name, cmd_params, raw, no_range, no_hazardous)
      else:
        if not prompt_for_script_abort():
          continue
    break
    return None

def cmd(*args):
  """Send a command to the specified target
  Usage:
    cmd(target_name, cmd_name, cmd_params = {})
  or
    cmd('target_name cmd_name with cmd_param1 value1, cmd_param2 value2')
  """
  return _cmd('cmd', 'cmd_no_hazardous_check', *args)

def cmd_no_range_check(*args):
  """Send a command to the specified target without range checking parameters
  Usage:
    cmd_no_range_check(target_name, cmd_name, cmd_params = {})
  or
    cmd_no_range_check('target_name cmd_name with cmd_param1 value1, cmd_param2 value2')
  """
  return _cmd('cmd_no_range_check', 'cmd_no_checks', *args)

def cmd_no_hazardous_check(*args):
  """Send a command to the specified target without hazardous checks
  Usage:
    cmd_no_hazardous_check(target_name, cmd_name, cmd_params = {})
  or
    cmd_no_hazardous_check('target_name cmd_name with cmd_param1 value1, cmd_param2 value2')
  """
  return _cmd('cmd_no_hazardous_check', None, *args)

def cmd_no_checks(*args):
  """Send a command to the specified target without range checking or hazardous checks
  Usage:
    cmd_no_checks(target_name, cmd_name, cmd_params = {})
  or
    cmd_no_checks('target_name cmd_name with cmd_param1 value1, cmd_param2 value2')
  """
  return _cmd('cmd_no_checks', None, *args)

def cmd_raw(*args):
  """Send a command to the specified target without running conversions
  Usage:
    cmd_raw(target_name, cmd_name, cmd_params = {})
  or
    cmd_raw('target_name cmd_name with cmd_param1 value1, cmd_param2 value2')
  """
  return _cmd('cmd_raw', 'cmd_raw_no_hazardous_check', *args)

def cmd_raw_no_range_check(*args):
  """Send a command to the specified target without range checking parameters or running conversions
  Usage:
    cmd_raw_no_range_check(target_name, cmd_name, cmd_params = {})
  or
    cmd_raw_no_range_check('target_name cmd_name with cmd_param1 value1, cmd_param2 value2')
  """
  return _cmd('cmd_raw_no_range_check', 'cmd_raw_no_checks', *args)

def cmd_raw_no_hazardous_check(*args):
  """Send a command to the specified target without hazardous checks or running conversions
  Usage:
    cmd_raw_no_hazardous_check(target_name, cmd_name, cmd_params = {})
  or
    cmd_raw_no_hazardous_check('target_name cmd_name with cmd_param1 value1, cmd_param2 value2')
  """
  return _cmd('cmd_raw_no_hazardous_check', None, *args)

def cmd_raw_no_checks(*args):
  """Send a command to the specified target without range checking or hazardous checks or running conversions
  Usage:
    cmd_raw_no_checks(target_name, cmd_name, cmd_params = {})
  or
    cmd_raw_no_checks('target_name cmd_name with cmd_param1 value1, cmd_param2 value2')
  """
  return _cmd('cmd_raw_no_checks', None, *args)

def send_raw(interface_name, data):
  """Sends raw data through an interface"""
  return cmd_tlm_server.write('send_raw', interface_name, data)

def send_raw_file(interface_name, filename):
  """Sends raw data through an interface from a file"""
  data = None
  with open(filename, 'rb') as file:
    data = file.read()
  return cmd_tlm_server.write('send_raw', interface_name, data)

def get_cmd_list(target_name):
  """Returns all the target commands as an array of arrays listing the command name and description."""
  return cmd_tlm_server.write('get_cmd_list', target_name)

def get_cmd_param_list(target_name, cmd_name):
  """Returns all the parameters for given command as an array of arrays
  containing the parameter name, default value, states, description, units
  full name, units abbreviation, and whether it is required."""
  return cmd_tlm_server.write('get_cmd_param_list', target_name, cmd_name)

def get_cmd_hazardous(target_name, cmd_name, cmd_params = None):
  """Returns whether a command is hazardous (true or false)"""
  if cmd_params == None:
    cmd_params = {}
  return cmd_tlm_server.write('get_cmd_hazardous', target_name, cmd_name, cmd_params)

def get_cmd_value(target_name, command_name, parameter_name, value_type = 'CONVERTED'):
  """Returns a value from the specified command"""
  return cmd_tlm_server.write('get_cmd_value', target_name, command_name, parameter_name, value_type)

def get_cmd_time(target_name = None, command_name = None):
  """Returns the time the most recent command was sent"""
  return cmd_tlm_server.write('get_cmd_time', target_name, command_name)

def get_cmd_buffer(target_name, command_name):
  """Returns the buffer from the most recent specified command"""
  return cmd_tlm_server.write('get_cmd_buffer', target_name, command_name)
