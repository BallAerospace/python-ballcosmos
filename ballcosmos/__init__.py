#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
__init__.py
"""

# Copyright 2021 Ball Aerospace & Technologies Corp.
# All Rights Reserved.
#
# This program is free software; you can modify and/or redistribute it
# under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; version 3 with
# attribution addendums as found in the LICENSE.txt

from ballcosmos.connection import *
from ballcosmos.environment import *

class CheckError(RuntimeError):
  pass

class StopScript(RuntimeError):
  pass

class SkipTestCase(RuntimeError):
  pass

class HazardousError(RuntimeError):
  pass

###################################

cmd_tlm_server = None
replay_mode_flag = False

###################################

def initialize_module():
  global cmd_tlm_server
  global replay_mode_flag

  if cmd_tlm_server:
    cmd_tlm_server.disconnect()

  if replay_mode_flag:
    cmd_tlm_server = Connection(DEFAULT_REPLAY_API_HOST, DEFAULT_REPLAY_API_PORT)
  else:
    cmd_tlm_server = Connection(DEFAULT_CTS_API_HOST, DEFAULT_CTS_API_PORT)


def shutdown():
  global cmd_tlm_server
  cmd_tlm_server.shutdown()


def disconnect():
  global cmd_tlm_server
  cmd_tlm_server.disconnect()


def set_replay_mode(replay_mode: bool):
  global replay_mode_flag
  if replay_mode is not replay_mode_flag:
    replay_mode_flag = replay_mode
    initialize_module()


def get_replay_mode():
  global replay_mode_flag
  return replay_mode_flag


initialize_module()

from ballcosmos.extract import *
from ballcosmos.scripting import *
from ballcosmos.telemetry import *
from ballcosmos.commands import *
from ballcosmos.cmd_tlm_server import *
from ballcosmos.replay import *
from ballcosmos.limits import *
from ballcosmos.tools import *
from ballcosmos.api_shared import *
