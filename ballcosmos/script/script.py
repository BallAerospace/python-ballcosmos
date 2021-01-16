import os

import ballcosmos.top_level
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
replay_mode_flag = False

DEFAULT_CTS_API_PORT = 7777
DEFAULT_REPLAY_API_PORT = 7877
DEFAULT_CTS_API_HOST = "127.0.0.1"
DEFAULT_REPLAY_API_HOST = "127.0.0.1"


def update_scope(scope: str):
    global cmd_tlm_server
    cmd_tlm_server.scope = str(scope)
    os.environ["COSMOS_SCOPE"] = str(scope)


def initialize_script_module(hostname=None, port=None, version=None):
    global cmd_tlm_server
    global replay_mode_flag

    try:
        os.environ["COSMOS_VERSION"]
    except KeyError:
        os.environ["COSMOS_VERSION"] = "5" if version is None else str(version)

    if cmd_tlm_server:
        cmd_tlm_server.disconnect()
    if hostname and port:
        cmd_tlm_server = JsonDRbObject(hostname, port)
    else:
        if replay_mode_flag:
            cmd_tlm_server = JsonDRbObject(
                DEFAULT_REPLAY_API_HOST, DEFAULT_REPLAY_API_PORT
            )
        else:
            cmd_tlm_server = JsonDRbObject(DEFAULT_CTS_API_HOST, DEFAULT_CTS_API_PORT)


def shutdown_cmd_tlm():
    cmd_tlm_server.shutdown()


def script_disconnect():
    cmd_tlm_server.disconnect()


def set_replay_mode(replay_mode, hostname=None, port=None, version=None):
    global replay_mode_flag
    if replay_mode != replay_mode_flag:
        replay_mode_flag = replay_mode
        initialize_script_module(hostname, port, version)


def get_replay_mode():
    global replay_mode_flag
    return replay_mode_flag


initialize_script_module()

from ballcosmos.script.extract import *
from ballcosmos.script.scripting import *
from ballcosmos.script.telemetry import *
from ballcosmos.script.commands import *
from ballcosmos.script.cmd_tlm_server import *
from ballcosmos.script.replay import *
from ballcosmos.script.limits import *
from ballcosmos.script.tools import *
from ballcosmos.script.api_shared import *
