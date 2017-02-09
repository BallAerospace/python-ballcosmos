import platform
import subprocess
from ballcosmos.json_drb_object import *
import ballcosmos.top_level
from ballcosmos.script.script import *

#######################################
# Methods accessing tlm_viewer
#######################################

def display(display_name, x_pos = None, y_pos = None, system_filename = 'system.txt', port = 7778):
  write_tlm_viewer('display', display_name, x_pos, y_pos, system_filename, port)

def clear(display_name, system_filename = 'system.txt', port = 7778):
  write_tlm_viewer('clear', display_name, None, None, system_filename, port)

def write_tlm_viewer(tlm_viewer_cmd, display_name, x_pos = None, y_pos = None, system_filename = 'system.txt', port = 7778):
  max_retries = 60
  retry_count = 0
  tlm_viewer = JsonDRbObject("localhost", port)
  while True:
    try:
      if tlm_viewer_cmd == 'display':
        tlm_viewer.write('display', display_name, x_pos, y_pos)
      else:
        tlm_viewer.write('clear', display_name)
      break
    except DRbConnError:
      # No Listening Tlm Viewer - So Start One
      canceled = cosmos_script_sleep(1)
      if not canceled:
        retry_count += 1
        start_tlm_viewer(system_filename)
        if retry_count < max_retries:
          continue
        else:
          raise RuntimeError("Unable to Successfully Start Listening Telemetry Viewer: {:s} could not be {:s}".format(display_name, action))
    except Exception as e:
      tlm_viewer.disconnect()
      raise e
  tlm_viewer.disconnect()

def start_tlm_viewer(system_file = 'system.txt'):
  mac_app = "/".join([ballcosmos.top_level.USERPATH, 'tools', 'mac', 'TlmViewer.app'])

  if platform.system == 'Darwin' and os.path.isfile(mac_app):
    subprocess.Popen("open '{:s}' --args --system {:s}".format(mac_app, system_file))
  else:
    cmd_name = 'ruby'
    if platform.system() == 'Windows':
      cmd_name += 'w' # Windows uses rubyw to avoid creating a DOS shell
    subprocess.Popen("{:s} '{:s}' --system {:s}".format(cmd_name, "/".join([ballcosmos.top_level.USERPATH, 'tools', 'TlmViewer']), system_file))
  cosmos_script_sleep(1)

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
