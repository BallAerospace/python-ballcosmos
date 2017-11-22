import platform
import subprocess
from ballcosmos.json_drb_object import *
import ballcosmos.top_level
from ballcosmos.script.script import *

#######################################
# Methods accessing script runner
#######################################

#~ def _ensure_script_runner_frame
  #~ yield if (defined? ScriptRunnerFrame) && ScriptRunnerFrame.instance

#~ def set_line_delay(delay)
  #~ _ensure_script_runner_frame { ScriptRunnerFrame.line_delay = delay if delay >= 0.0 }

#~ def get_line_delay
  #~ _ensure_script_runner_frame { ScriptRunnerFrame.line_delay }

#~ def get_scriptrunner_message_log_filename
  #~ filename = nil
  #~ _ensure_script_runner_frame do
    #~ filename = ScriptRunnerFrame.instance.message_log.filename if ScriptRunnerFrame.instance.message_log
  #~ return filename

#~ def start_new_scriptrunner_message_log
  #~ # A new log will be created at the next message
  #~ _ensure_script_runner_frame { ScriptRunnerFrame.instance.stop_message_log }

#~ def disable_instrumentation
  #~ if (defined? ScriptRunnerFrame) && ScriptRunnerFrame.instance
    #~ ScriptRunnerFrame.instance.use_instrumentation = false
    #~ begin
      #~ yield
    #~ ensure
      #~ ScriptRunnerFrame.instance.use_instrumentation = true
  #~ else
    #~ yield

#~ def set_stdout_max_lines(max_lines)
  #~ _ensure_script_runner_frame { ScriptRunnerFrame.instance.stdout_max_lines = max_lines }

#######################################
# Methods for debugging
#######################################

#~ def insert_return(*params)
  #~ _ensure_script_runner_frame do
    #~ ScriptRunnerFrame.instance.inline_return = true
    #~ ScriptRunnerFrame.instance.inline_return_params = params

#~ def step_mode
  #~ _ensure_script_runner_frame { ScriptRunnerFrame.step_mode = true }

#~ def run_mode
  #~ _ensure_script_runner_frame { ScriptRunnerFrame.step_mode = false }

#~ def show_backtrace(value = true)
  #~ _ensure_script_runner_frame { ScriptRunnerFrame.show_backtrace = value }

###########################
# Telemetry Screen methods
###########################

# Get the organized list of available telemetry screens
def get_screen_list(config_filename = None, force_refresh = False):
  return ballcosmos.script.script.cmd_tlm_server.write('get_screen_list', config_filename, force_refresh)

# Get a specific screen definition
def get_screen_definition(screen_full_name, config_filename = None, force_refresh = False):
  return ballcosmos.script.script.cmd_tlm_server.write('get_screen_definition', screen_full_name, config_filename, force_refresh)
