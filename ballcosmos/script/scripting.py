import time
import os
import logging
from os import listdir
from os.path import isfile, isdir
from ballcosmos.script.script import *

DEFAULT_TLM_POLLING_RATE = 0.25

def play_wav_file(wav_filename):
  pass
  #~ Cosmos.play_wav_file(wav_filename)

def status_bar(message):
  pass
  #~ if defined? ScriptRunner
    #~ script_runner = nil
    #~ ObjectSpace.each_object {|object| if ScriptRunner === object then script_runner = object; break; end}
    #~ script_runner.script_set_status(message) if script_runner

def ask_string(question, blank_or_default = False, password = False):
  answer = ''
  default = ''
  if blank_or_default != True and blank_or_default != False:
    question += " (default = {:s})".format(str(blank_or_default))
    allow_blank = True
  else:
    allow_blank = blank_or_default
  while not answer:
    answer = input(question + " ")
    if allow_blank:
      break
  if not answer and default:
    answer = default
  return answer

def ask(question, blank_or_default = False, password = False):
  string = ask_string(question, blank_or_default, password)
  value = convert_to_value(string)
  return value

def prompt(string):
  prompt_to_continue(string)

def message_box(string, *buttons):
  prompt_message_box(string, buttons)

def vertical_message_box(string, *buttons):
  prompt_vertical_message_box(string, buttons)

def combo_box(string, *options):
  prompt_combo_box(string, options)

def _file_dialog(message, directory, select_files = True):
  answer = ''
  if select_files:
    files = [f for f in listdir(directory) if isfile(os.path.join(directory, f))]
  else:
    files = [f for f in listdir(directory) if isdir(os.path.join(directory, f))]
  while not answer:
    answer = input(message + "\n" + "\n".join(files) + "\n<Type file name>:")
  return answer

def save_file_dialog(directory = ballcosmos.top_level.USERPATH, message = "Save File"):
  _file_dialog(message, directory)

def open_file_dialog(directory =  ballcosmos.top_level.USERPATH, message = "Open File"):
  _file_dialog(message, directory)

def open_files_dialog(directory =  ballcosmos.top_level.USERPATH, message = "Open File(s)"):
  _file_dialog(message, directory)

def open_directory_dialog(directory =  ballcosmos.top_level.USERPATH, message = "Open Directory"):
  _file_dialog(message, directory, False)

def _upcase(target_name, packet_name, item_name):
  """Creates a string with the parameters upcased"""
  return "{:s} {:s} {:s}".format(target_name.upper(), packet_name.upper(), item_name.upper())

def _check(method, *args):
  """Implementaiton of the various check commands. It yields back to the
  caller to allow the return of the value through various telemetry calls.
  This method should not be called directly by application code."""
  target_name, packet_name, item_name, comparison_to_eval = check_process_args(args, 'check')
  value = method(target_name, packet_name, item_name)
  if comparison_to_eval:
    return check_eval(target_name, packet_name, item_name, comparison_to_eval, value)
  else:
    logger = logging.getLogger('ballcosmos')
    logger.info("CHECK: {:s} == {:s}".format(_upcase(target_name, packet_name, item_name, str(value))))

def check(*args):
  """Check the converted value of a telmetry item against a condition
  Always print the value of the telemetry item to STDOUT
  If the condition check fails, raise an error
  Supports two signatures:
  check(target_name, packet_name, item_name, comparison_to_eval)
  or
  check('target_name packet_name item_name > 1')
  """
  return _check(ballcosmos.script.telemetry.tlm, *args)

def check_formatted(*args):
  """Check the formatted value of a telmetry item against a condition
  Always print the value of the telemetry item to STDOUT
  If the condition check fails, raise an error
  Supports two signatures:
  check(target_name, packet_name, item_name, comparison_to_eval)
  or
  check('target_name packet_name item_name > 1')
  """
  return _check(ballcosmos.script.telemetry.tlm_formatted, *args)

def check_with_units(*args):
  """Check the formatted with units value of a telmetry item against a condition
  Always print the value of the telemetry item to STDOUT
  If the condition check fails, raise an error
  Supports two signatures:
  check(target_name, packet_name, item_name, comparison_to_eval)
  or
  check('target_name packet_name item_name > 1')
  """
  return _check(ballcosmos.script.telemetry.tlm_with_units, *args)

def check_raw(*args):
  """Check the raw value of a telmetry item against a condition
  Always print the value of the telemetry item to STDOUT
  If the condition check fails, raise an error
  Supports two signatures:
  check(target_name, packet_name, item_name, comparison_to_eval)
  or
  check('target_name packet_name item_name > 1')
  """
  return _check(ballcosmos.script.telemetry.tlm_raw, *args)

def _check_tolerance(method, *args):
  target_name, packet_name, item_name, expected_value, tolerance = check_tolerance_process_args(args, 'check_tolerance')
  value = method(target_name, packet_name, item_name)
  range_bottom = expected_value - tolerance
  range_top = expected_value + tolerance
  check_str = "CHECK: {:s}".format(_upcase(target_name, packet_name, item_name))
  range_str = "range {:g} to {:g} with value == {:g}".format(range_bottom, range_top, value)
  if value >= range_bottom and value <= range_top:
    logger = logging.getLogger('ballcosmos')
    logger.info("{:s} was within {:s}".format(check_str, range_str))
  else:
    message = "{:s} failed to be within {:s}".format(check_str, range_str)
    raise CheckError(message)

def check_tolerance(*args):
  """Check the converted value of a telmetry item against an expected value with a tolerance
  Always print the value of the telemetry item to STDOUT
  If the condition check fails, raise an error
  Supports two signatures:
  check_tolerance(target_name, packet_name, item_name, expected_value, tolerance)
  or
  check_tolerance('target_name packet_name item_name', expected_value, tolerance)
  """
  return _check_tolerance(ballcosmos.script.telemetry.tlm, *args)

def check_tolerance_raw(*args):
  """Check the raw value of a telmetry item against an expected value with a tolerance
  Always print the value of the telemetry item to STDOUT
  If the condition check fails, raise an error
  Supports two signatures:
  check_tolerance_raw(target_name, packet_name, item_name, expected_value, tolerance)
  or
  check_tolerance_raw('target_name packet_name item_name', expected_value, tolerance)
  """
  return _check_tolerance(ballcosmos.script.telemetry.tlm_raw, *args)

def check_expression(exp_to_eval, locals = None):
  """Check to see if an expression is true without waiting.  If the expression
  is not true, the script will pause."""
  success = cosmos_script_wait_implementation_expression(exp_to_eval, 0, DEFAULT_TLM_POLLING_RATE, locals)
  if success:
    logger = logging.getLogger('ballcosmos')
    logger.info("CHECK: {:s} is TRUE".format(exp_to_eval))
  else:
    message = "CHECK: {:s} is FALSE".format(exp_to_eval)
    raise CheckError(message)

def wait(*args):
  """Wait on an expression to be true.  On a timeout, the script will continue.
  Supports multiple signatures:
  wait(time)
  wait('target_name packet_name item_name > 1', timeout, polling_rate)
  wait('target_name', 'packet_name', 'item_name', comparison_to_eval, timeout, polling_rate)
  """
  wait_process_args(args, 'wait', 'CONVERTED')

def wait_raw(*args):
  """Wait on an expression to be true.  On a timeout, the script will continue.
  Supports multiple signatures:
  wait(time)
  wait_raw('target_name packet_name item_name > 1', timeout, polling_rate)
  wait_raw('target_name', 'packet_name', 'item_name', comparison_to_eval, timeout, polling_rate)"""
  wait_process_args(args, 'wait_raw', 'RAW')

def _wait_tolerance(raw, *args):
  if raw:
    type = 'RAW'
  else:
    type = 'CONVERTED'
  type_string = 'wait_tolerance'
  if raw:
    type_string += '_raw'
  target_name, packet_name, item_name, expected_value, tolerance, timeout, polling_rate = wait_tolerance_process_args(args, type_string)
  start_time = time.time()
  success, value = cosmos_script_wait_implementation_tolerance(target_name, packet_name, item_name, type, expected_value, tolerance, timeout, polling_rate)
  time_float = time.time() - start_time
  range_bottom = expected_value - tolerance
  range_top = expected_value + tolerance
  wait_str = "WAIT: {:s}".format(_upcase(target_name, packet_name, item_name))
  range_str = "range {:g} to {:g} with value == {:g} after waiting {:g} seconds".format(range_bottom, range_top, value, time_float)
  logger = logging.getLogger('ballcosmos')
  if success:
    logger.info("{:s} was within {:s}".format(wait_str, range_str))
  else:
    logger.warning("{:s} failed to be within {:s}".format(wait_str, range_str))
  return time_float

def wait_tolerance(*args):
  """Wait on an expression to be true.  On a timeout, the script will continue.
  Supports multiple signatures:
  wait_tolerance('target_name packet_name item_name', expected_value, tolerance, timeout, polling_rate)
  wait_tolerance('target_name', 'packet_name', 'item_name', expected_value, tolerance, timeout, polling_rate)
  """
  return _wait_tolerance(False, *args)

def wait_tolerance_raw(*args):
  """Wait on an expression to be true.  On a timeout, the script will continue.
  Supports multiple signatures:
  wait_tolerance_raw('target_name packet_name item_name', expected_value, tolerance, timeout, polling_rate)
  wait_tolerance_raw('target_name', 'packet_name', 'item_name', expected_value, tolerance, timeout, polling_rate)
  """
  return _wait_tolerance(True, *args)

def wait_expression(exp_to_eval, timeout, polling_rate = DEFAULT_TLM_POLLING_RATE, locals = None):
  """Wait on a custom expression to be true"""
  start_time = time.time()
  success = cosmos_script_wait_implementation_expression(exp_to_eval, timeout, polling_rate, locals)
  time_float = time.time() - start_time
  logger = logging.getLogger('ballcosmos')
  if success:
    logger.info("WAIT: {:s} is TRUE after waiting {:g} seconds".format(exp_to_eval, time_float))
  else:
    logger.warning("WAIT: {:s} is FALSE after waiting {:g} seconds".format(exp_to_eval, time_float))
  return time_float

def _wait_check(raw, *args):
  if raw:
    type = 'RAW'
  else:
    type = 'CONVERTED'
  target_name, packet_name, item_name, comparison_to_eval, timeout, polling_rate = wait_check_process_args(args, 'wait_check')
  start_time = time.time()
  success, value = cosmos_script_wait_implementation(target_name, packet_name, item_name, type, comparison_to_eval, timeout, polling_rate)
  time_float = time.time() - start_time
  check_str = "CHECK: {:s} {:s}".format(_upcase(target_name, packet_name, item_name), comparison_to_eval)
  with_value_str = "with value == {:s} after waiting {:g} seconds".format(str(value), time_float)
  if success:
    logger = logging.getLogger('ballcosmos')
    logger.info("{:s} success {:s}".format(check_str, with_value_str))
  else:
    message = "{:s} failed {:s}".format(check_str, with_value_str)
    raise CheckError(message)
  return time_float

def wait_check(*args):
  """Wait for the converted value of a telmetry item against a condition or for a timeout
  and then check against the condition
  Supports two signatures:
  wait_check(target_name, packet_name, item_name, comparison_to_eval, timeout, polling_rate)
  or
  wait_check('target_name packet_name item_name > 1', timeout, polling_rate)"""
  return _wait_check(False, *args)

def wait_check_raw(*args):
  """Wait for the raw value of a telmetry item against a condition or for a timeout
  and then check against the condition
  Supports two signatures:
  wait_check_raw(target_name, packet_name, item_name, comparison_to_eval, timeout, polling_rate)
  or
  wait_check_raw('target_name packet_name item_name > 1', timeout, polling_rate)"""
  return _wait_check(True, *args)

def _wait_check_tolerance(raw, *args):
  type_string = 'wait_check_tolerance'
  if raw:
    type_string += '_raw'
  if raw:
    type = 'RAW'
  else:
    type = 'CONVERTED'
  target_name, packet_name, item_name, expected_value, tolerance, timeout, polling_rate = wait_tolerance_process_args(args, type_string)
  start_time = time.time()
  success, value = cosmos_script_wait_implementation_tolerance(target_name, packet_name, item_name, type, expected_value, tolerance, timeout, polling_rate)
  time_float = time.time() - start_time
  range_bottom = expected_value - tolerance
  range_top = expected_value + tolerance
  check_str = "CHECK: {:s}".format(_upcase(target_name, packet_name, item_name))
  range_str = "range {:g} to {:g} with value == {:g} after waiting {:g} seconds".format(range_bottom, range_top, value, time_float)
  if success:
    logger = logging.getLogger('ballcosmos')
    logger.info("{:s} was within {:s}".format(check_str, range_str))
  else:
    message = "{:s} failed to be within {:s}".format(check_str, range_str)
    raise CheckError(message)
  return time_float

def wait_check_tolerance(*args):
  _wait_check_tolerance(False, *args)

def wait_check_tolerance_raw(*args):
  _wait_check_tolerance(True, *args)

def wait_check_expression(exp_to_eval,
                          timeout,
                          polling_rate = DEFAULT_TLM_POLLING_RATE,
                          context = None):
  """Wait on an expression to be true.  On a timeout, the script will pause"""
  start_time = time.time()
  success = cosmos_script_wait_implementation_expression(exp_to_eval,
                                                         timeout,
                                                         polling_rate,
                                                         context)
  time_float = time.time() - start_time
  if success:
    logger = logging.getLogger('ballcosmos')
    logger.info("CHECK: {:s} is TRUE after waiting {:g} seconds".format(exp_to_eval, time_float))
  else:
    message = "CHECK: {:s} is FALSE after waiting {:g} seconds".format(exp_to_eval, time_float)
    raise CheckError(message)
  return time_float

def wait_expression_stop_on_timeout(*args):
  return wait_check_expression(*args)

def _wait_packet(check,
                 target_name,
                 packet_name,
                 num_packets,
                 timeout,
                 polling_rate = DEFAULT_TLM_POLLING_RATE):
  """Wait for a telemetry packet to be received a certain number of times or timeout"""
  if check:
    type = 'CHECK'
  else:
    type = 'WAIT'
  initial_count = ballcosmos.script.telemetry.tlm(target_name, packet_name, 'RECEIVED_COUNT')
  start_time = time.time()
  success, value = cosmos_script_wait_implementation(target_name,
                                                     packet_name,
                                                     'RECEIVED_COUNT',
                                                     'CONVERTED',
                                                     ">= {:d}".format(initial_count + num_packets),
                                                     timeout,
                                                     polling_rate)
  time_float = time.time() - start_time
  logger = logging.getLogger('ballcosmos')
  if success:
    logger.info("{:s}: {:s} {:s} received {:d} times after waiting {:g} seconds".format(type, target_name.upper(), packet_name.upper(), value - initial_count, time_float))
  else:
    message = "{:s}: {:s} {:s} expected to be received {:d} times but only received {:d} times after waiting {:g} seconds".format(type, target_name.upper(), packet_name.upper(), num_packets, value - initial_count, time_float)
    if check:
      raise CheckError(message)
    else:
      logger.warning(message)
  return time_float

def wait_packet(target_name,
                packet_name,
                num_packets,
                timeout,
                polling_rate = DEFAULT_TLM_POLLING_RATE):
  return _wait_packet(False, target_name, packet_name, num_packets, timeout, polling_rate)

def wait_check_packet(target_name,
                      packet_name,
                      num_packets,
                      timeout,
                      polling_rate = DEFAULT_TLM_POLLING_RATE):
  """Wait for a telemetry packet to be received a certain number of times or timeout and raise an error"""
  return _wait_packet(True, target_name, packet_name, num_packets, timeout, polling_rate)

#~ def _get_procedure_path(procedure_name):
  #~ # Handle not-giving an extension
  #~ procedure_name_with_extension = None
  #~ if File.extname(procedure_name).empty?
    #~ procedure_name_with_extension = procedure_name + '.rb'

  #~ path = None

  #~ # Find filename in search path
  #~ ($:).each do |directory|
    #~ if File.exist?(directory + '/' + procedure_name) and not File.directory?(directory + '/' + procedure_name)
      #~ path = directory + '/' + procedure_name
      #~ break

    #~ if procedure_name_with_extension and File.exist?(directory + '/' + procedure_name_with_extension)
      #~ procedure_name = procedure_name_with_extension
      #~ path = directory + '/' + procedure_name
      #~ break

  #~ # Handle absolute path
  #~ path = procedure_name if !path and File.exist?(procedure_name)
  #~ path = procedure_name_with_extension if !path and procedure_name_with_extension and File.exist?(procedure_name_with_extension)

  #~ raise LoadError, "Procedure not found -- #{procedure_name}" unless path
  #~ path

#~ def check_file_cache_for_instrumented_script(path, md5)
  #~ instrumented_script = nil
  #~ cached = true
  #~ use_file_cache = true

  #~ Cosmos.set_working_dir do
    #~ cache_path = File.join(System.paths['TMP'], 'script_runner')
    #~ unless File.directory?(cache_path)
      #~ # Try to create .cache directory
      #~ begin
        #~ Dir.mkdir(cache_path)
      #~ rescue
        #~ use_file_cache = false
      #~ end
    #~ end

    #~ cache_filename = nil
    #~ if use_file_cache
      #~ # Check file based instrumented cache
      #~ flat_path = path.tr("/", "_").gsub("\\", "_").tr(":", "_").tr(" ", "_")
      #~ flat_path_with_md5 = flat_path + '_' + md5
      #~ cache_filename = File.join(cache_path, flat_path_with_md5)
    #~ end

    #~ if use_file_cache and File.exist?(cache_filename)
      #~ # Use file cached instrumentation
      #~ File.open(cache_filename, 'r') {|file| instrumented_script = file.read}
    #~ else
      #~ cached = false

      #~ # Build instrumentation
      #~ file_text = ''
      #~ begin
        #~ file_text = File.read(path)
      #~ rescue Exception => error
        #~ raise "Error reading procedure file : #{path}"
      #~ end

      #~ instrumented_script = ScriptRunnerFrame.instrument_script(file_text, path, true)

      #~ # Cache instrumentation into file
      #~ if use_file_cache
        #~ begin
          #~ File.open(cache_filename, 'w') {|file| file.write(instrumented_script)}
        #~ rescue
          #~ # Oh well, failed to write cache file
        #~ end
      #~ end
    #~ end
  #~ end
  #~ [instrumented_script, cached]
#~ end

#~ def start(procedure_name)
  #~ cached = true
  #~ path = _get_procedure_path(procedure_name)

  #~ if defined? ScriptRunnerFrame and ScriptRunnerFrame.instance
    #~ md5 = nil
    #~ begin
      #~ md5 = Cosmos.md5_files([path]).hexdigest
    #~ rescue Exception => error
      #~ raise "Error calculating md5 on procedure file : #{path}"
    #~ end

    #~ # Check RAM based instrumented cache
    #~ instrumented_cache = ScriptRunnerFrame.instrumented_cache[path]
    #~ instrumented_script = nil
    #~ if instrumented_cache and md5 == instrumented_cache[1]
      #~ # Use cached instrumentation
      #~ instrumented_script = instrumented_cache[0]
    #~ else
      #~ instrumented_script, cached = check_file_cache_for_instrumented_script(path, md5)
      #~ # Cache instrumentation into RAM
      #~ ScriptRunnerFrame.instrumented_cache[path] = [instrumented_script, md5]
    #~ end

    #~ Object.class_eval(instrumented_script, path, 1)
  #~ else # No ScriptRunnerFrame so just start it locally
    #~ cached = false
    #~ begin
      #~ Kernel::load(path)
    #~ rescue LoadError => error
      #~ raise LoadError, "Error loading -- #{procedure_name}\n#{error.message}"
    #~ end
  #~ end
  #~ # Return whether we had to load and instrument this file, i.e. it was not cached
  #~ !cached
#~ end

#~ # Require an additional ruby file
#~ def load_utility(procedure_name)
  #~ not_cached = false
  #~ if defined? ScriptRunnerFrame and ScriptRunnerFrame.instance
    #~ saved = ScriptRunnerFrame.instance.use_instrumentation
    #~ begin
      #~ ScriptRunnerFrame.instance.use_instrumentation = false
      #~ not_cached = start(procedure_name)
    #~ ensure
      #~ ScriptRunnerFrame.instance.use_instrumentation = saved
    #~ end
  #~ else # Just call start
    #~ not_cached = start(procedure_name)
  #~ end
  #~ # Return whether we had to load and instrument this file, i.e. it was not cached
  #~ # This is designed to match the behavior of Ruby's require and load keywords
  #~ not_cached
#~ end
#~ alias require_utility load_utility

##########################################
# Protected Methods
##########################################

def check_process_args(args, function_name):
  length = len(args)
  if length == 1:
    target_name, packet_name, item_name, comparison_to_eval = extract_fields_from_check_text(args[0])
  elif length == 4:
    target_name = args[0]
    packet_name = args[1]
    item_name = args[2]
    comparison_to_eval = args[3]
  else:
    # Invalid number of arguments
    raise RuntimeError("ERROR: Invalid number of arguments ({:d}) passed to {:s}()".format(len(args), function_name))
  return [target_name, packet_name, item_name, comparison_to_eval]

def check_tolerance_process_args(args, function_name):
  length = len(args)
  if length == 3:
    target_name, packet_name, item_name = extract_fields_from_tlm_text(args[0])
    expected_value = args[1]
    tolerance = abs(args[2])
  elif length == 5:
    target_name = args[0]
    packet_name = args[1]
    item_name = args[2]
    expected_value = args[3]
    tolerance = abs(args[4])
  else:
    # Invalid number of arguments
    raise RuntimeError("ERROR: Invalid number of arguments ({:d}) passed to {:s}()".format(length, function_name))
  return [target_name, packet_name, item_name, expected_value, tolerance]

def _execute_wait(target_name, packet_name, item_name, value_type, comparison_to_eval, timeout, polling_rate):
  start_time = time.time()
  success, value = cosmos_script_wait_implementation(target_name, packet_name, item_name, value_type, comparison_to_eval, timeout, polling_rate)
  time_float = time.time() - start_time
  wait_str = "WAIT: {:s} {:s}".format(_upcase(target_name, packet_name, item_name), comparison_to_eval)
  value_str = "with value == {:s} after waiting {:g} seconds".format(str(value), time_float)
  logger = logging.getLogger('ballcosmos')
  if success:
    logger.info("{:s} success {:s}".format(wait_str, value_str))
  else:
    logger.warning("{:s} failed {:s}".format(wait_str, value_str))

def wait_process_args(args, function_name, value_type):
  time_float = None

  logger = logging.getLogger('ballcosmos')
  length = len(args)
  if length == 0:
    start_time = time.time()
    cosmos_script_sleep()
    time_float = time.time() - start_time
    logger.info("WAIT: Indefinite for actual time of {:g} seconds".format(time_float))

  elif length == 1:
    try:
      value = float(args[0])
    except ValueError:
      raise RuntimeError("Non-numeric wait time specified")

    start_time = time.time()
    cosmos_script_sleep(value)
    time_float = time.time() - start_time
    logger.info("WAIT: {:g} seconds with actual time of {:g} seconds".format(value, time_float))

  elif length == 2 or length == 3:
    target_name, packet_name, item_name, comparison_to_eval = extract_fields_from_check_text(args[0])
    timeout = args[1]
    if length == 3:
      polling_rate = args[2]
    else:
      polling_rate = DEFAULT_TLM_POLLING_RATE
    _execute_wait(target_name, packet_name, item_name, value_type, comparison_to_eval, timeout, polling_rate)

  elif length == 5 or length == 6:
    target_name = args[0]
    packet_name = args[1]
    item_name = args[2]
    comparison_to_eval = args[3]
    timeout = args[4]
    if length == 6:
      polling_rate = args[5]
    else:
      polling_rate = DEFAULT_TLM_POLLING_RATE
    _execute_wait(target_name, packet_name, item_name, value_type, comparison_to_eval, timeout, polling_rate)
  else:
    # Invalid number of arguments
    raise RuntimeError("ERROR: Invalid number of arguments ({:d}) passed to {:s}()".format(length, function_name))
  return time_float

def wait_tolerance_process_args(args, function_name):
  length = len(args)
  if length == 4 or length == 5:
    target_name, packet_name, item_name = extract_fields_from_tlm_text(args[0])
    expected_value = args[1]
    tolerance = abs(args[2])
    timeout = args[3]
    if length == 5:
      polling_rate = args[4]
    else:
      polling_rate = DEFAULT_TLM_POLLING_RATE
  elif length == 6 or length == 7:
    target_name = args[0]
    packet_name = args[1]
    item_name = args[2]
    expected_value = args[3]
    tolerance = abs(args[4])
    timeout = args[5]
    if length == 7:
      polling_rate = args[6]
    else:
      polling_rate = DEFAULT_TLM_POLLING_RATE
  else:
    # Invalid number of arguments
    raise RuntimeError("ERROR: Invalid number of arguments ({:d}) passed to {:s}()".format(length, function_name))
  return [target_name, packet_name, item_name, expected_value, tolerance, timeout, polling_rate]

def wait_check_process_args(args, function_name):
  length = len(args)
  if length == 2 or length == 3:
    target_name, packet_name, item_name, comparison_to_eval = extract_fields_from_check_text(args[0])
    timeout = args[1]
    if length == 3:
      polling_rate = args[2]
    else:
      polling_rate = DEFAULT_TLM_POLLING_RATE
  elif length == 5 or length == 6:
    target_name = args[0]
    packet_name = args[1]
    item_name = args[2]
    comparison_to_eval = args[3]
    timeout = args[4]
    if length == 6:
      polling_rate = args[5]
    else:
      polling_rate = DEFAULT_TLM_POLLING_RATE
  else:
    # Invalid number of arguments
    raise RuntimeError("ERROR: Invalid number of arguments ({:d}) passed to {:s}()".format(length, function_name))
  return [target_name, packet_name, item_name, comparison_to_eval, timeout, polling_rate]

def cosmos_script_sleep(sleep_time = None):
  """sleep in a script - returns true if canceled mid sleep"""
  if sleep_time:
    time.sleep(sleep_time)
  else:
    input('Infinite Wait - Press Enter to Continue: ')
  return False

def _cosmos_script_wait_implementation(target_name, packet_name, item_name, value_type, timeout, polling_rate, exp_to_eval):
  end_time = time.time() + timeout

  while True:
    work_start = time.time()
    value = ballcosmos.script.telemetry.tlm_variable(target_name, packet_name, item_name, value_type)
    if eval(exp_to_eval):
      return [True, value]
    if time.time() >= end_time:
      break

    delta = time.time() - work_start
    sleep_time = polling_rate - delta
    end_delta = end_time - time.time()
    if end_delta < sleep_time:
      sleep_time = end_delta
    if sleep_time < 0:
      sleep_time = 0
    canceled = cosmos_script_sleep(sleep_time)

    if canceled:
      value = tlm_variable(target_name, packet_name, item_name, value_type)
      if eval(exp_to_eval):
        return [True, value]
      else:
        return [False, value]

  return [False, value]

# Wait for a converted telemetry item to pass a comparison
def cosmos_script_wait_implementation(target_name, packet_name, item_name, value_type, comparison_to_eval, timeout, polling_rate = DEFAULT_TLM_POLLING_RATE):
  exp_to_eval = "value " + comparison_to_eval
  return _cosmos_script_wait_implementation(target_name, packet_name, item_name, value_type, timeout, polling_rate, exp_to_eval)

def cosmos_script_wait_implementation_tolerance(target_name, packet_name, item_name, value_type, expected_value, tolerance, timeout, polling_rate = DEFAULT_TLM_POLLING_RATE):
  exp_to_eval = "(value >= ({:g} - {:g}) and value <= ({:g} + {:g}))".format(expected_value, abs(tolerance), abs(tolerance), expected_value)
  return _cosmos_script_wait_implementation(target_name, packet_name, item_name, value_type, timeout, polling_rate, exp_to_eval)

def cosmos_script_wait_implementation_expression(exp_to_eval, timeout, polling_rate, locals = None):
  """Wait on an expression to be true."""
  end_time = time.time() + timeout
  #~ context = ScriptRunnerFrame.instance.script_binding if !context and defined? ScriptRunnerFrame and ScriptRunnerFrame.instance

  while True:
    work_start = time.time()
    if eval(exp_to_eval, locals):
      return True
    if time.time() >= end_time:
      break

    delta = time.time() - work_start
    sleep_time = polling_rate - delta
    end_delta = end_time - time.time()
    if end_delta < sleep_time:
      sleep_time = end_delta
    if sleep_time < 0:
      sleep_time = 0
    canceled = cosmos_script_sleep(sleep_time)

    if canceled:
      if eval(exp_to_eval, locals):
        return True
      else:
        return None

  return None

def check_eval(target_name, packet_name, item_name, comparison_to_eval, value):
  string = "value " + comparison_to_eval
  check_str = "CHECK: {:s} {:s}".format(_upcase(target_name, packet_name, item_name), comparison_to_eval)
  value_str = "with value == {:s}".format(str(value))
  if eval(string):
    logger = logging.getLogger('ballcosmos')
    logger.info("{:s} success {:s}".format(check_str, value_str))
  else:
    message = "{:s} failed {:s}".format(check_str, value_str)
    raise CheckError(message)

def build_cmd_output_string(target_name, cmd_name, cmd_params, raw = False):
  if raw:
    output_string = 'cmd_raw("'
  else:
    output_string = 'cmd("'
  output_string += target_name + ' ' + cmd_name
  if cmd_params == None or len(cmd_params) == 0:
    output_string += '")'
  else:
    params = []
    for key, value in cmd_params.items():
      if isinstance(value, str):
        if isinstance(convert_to_value(value), str):
          value = repr(value)
          if len(value) > 256:
            value = value[0:256] + "...'"
          value = value.replace('"',"'")
      params.append("{:s} {:s}".format(key, str(value)))
    params = (", ").join(params)
    output_string += ' with ' + params + '")'
  return output_string

def prompt_for_hazardous(target_name, cmd_name, hazardous_description):
  message = "Warning: Command {:s} {:s} is Hazardous. ".format(target_name, cmd_name)
  if hazardous_description:
    message += "\n{:s}\n".format(hazardous_description)
  message += "Send? (y,n): "
  answer = input(message)
  if answer.lower() == 'y':
    return True
  else:
    return False

def prompt_for_script_abort():
  answer = input("Stop running script? (y,n): ")
  if answer.downcase == 'y':
    exit()
  else:
    return False # Not aborted - Retry

def prompt_to_continue(string):
  return input("{:s}: ".format(string))

def prompt_message_box(string, buttons):
  return input("{:s} ({:s}): ".format(string, ", ".join(buttons)))

def prompt_vertical_message_box(string, options):
  prompt_message_box(string, options)

def prompt_combo_box(string, options):
  prompt_message_box(string, options)
