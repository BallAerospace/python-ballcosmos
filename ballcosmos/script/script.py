from ballcosmos.json_drb_object import *

class CheckError(RuntimeError):
  pass

class StopScript(RuntimeError):
  pass

class SkipTestCase(RuntimeError):
  pass

class HazardousError(RuntimeError):
  pass

cmd_tlm_server = None

def initialize_script_module(hostname = '127.0.0.1', port = 7777):
  global cmd_tlm_server
  cmd_tlm_server = JsonDRbObject(hostname, port)

def shutdown_cmd_tlm():
  cmd_tlm_server.shutdown()

def script_disconnect():
  cmd_tlm_server.disconnect()

initialize_script_module()

import ballcosmos.top_level
from ballcosmos.script.extract import *
from ballcosmos.script.scripting import *
from ballcosmos.script.telemetry import *
from ballcosmos.script.commands import *
from ballcosmos.script.cmd_tlm_server import *
from ballcosmos.script.limits import *
from ballcosmos.script.tools import *
