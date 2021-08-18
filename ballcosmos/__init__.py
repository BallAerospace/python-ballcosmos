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

CTS = None  # Stands for command telemetry server
RMF = False

###################################


def initialize_module(hostname: str, port: int):
    global CTS
    global RMF

    if CTS:
        CTS.disconnect()

    if hostname and port:
        CTS = Connection(hostname, port)
    elif RMF:
        CTS = Connection(DEFAULT_REPLAY_API_HOST, DEFAULT_REPLAY_API_PORT)
    else:
        CTS = Connection(DEFAULT_CTS_API_HOST, DEFAULT_CTS_API_PORT)


def shutdown():
    """shutdown the connection"""
    global CTS
    CTS.shutdown()


def disconnect():
    """disconnect from the server"""
    global CTS
    CTS.disconnect()


def set_replay_mode(replay_mode: bool):
    """Set replay mode to True or False"""
    global RMF
    if replay_mode is not RMF:
        RMF = replay_mode
        initialize_module()


def get_replay_mode():
    """Get RMF, True or False"""
    global RMF
    return RMF


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
