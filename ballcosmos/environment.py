#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
environment.py
"""

# Copyright 2021 Ball Aerospace & Technologies Corp.
# All Rights Reserved.
#
# This program is free software; you can modify and/or redistribute it
# under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; version 3 with
# attribution addendums as found in the LICENSE.txt

import os

from ballcosmos import __name__, __version__


_cosmos_version = "COSMOS_VERSION"

_default_scope = "COSMOS_SCOPE"

_default_hostname = "COSMOS_HOSTNAME"

_default_port = "COSMOS_PORT"

_default_replay_hostname = "COSMOS_REPLAY_HOSTNAME"

_default_replay_port = "COSMOS_REPLAY_PORT"

_json_rpc_version = "COSMOS_JSON_RPC_VERSION"

_log_level = "COSMOS_LOG_LEVEL"

_max_retry_count = "COSMOS_MAX_RETRY_COUNT"

_user_agent = "COSMOS_USER_AGENT"

_cosmos_token = "COSMOS_TOKEN"

COSMOS_HOSTNAME = os.environ.get(_default_hostname, "127.0.0.1")

COSMOS_PORT = os.environ.get(_default_port, "2900")

COSMOS_V4_REPLAY_HOSTNAME = os.environ.get(_default_replay_hostname, "127.0.0.1")

COSMOS_V4_REPLAY_PORT = os.environ.get(_default_replay_port, "7877")

COSMOS_SCOPE = os.environ.get(_default_scope, "DEFAULT")

COSMOS_TOKEN = os.environ.get(_cosmos_token, "SuperSecret")

COSMOS_VERSION = os.environ.get(_cosmos_version, "5")

JSON_RPC_VERSION = os.environ.get(_json_rpc_version, "2.0")

LOG_LEVEL = os.environ.get(_log_level, "INFO")

try:
    MAX_RETRY_COUNT = int(os.environ.get(_max_retry_count))
except TypeError:
    MAX_RETRY_COUNT = 3

_default_user_agent = [
    "{}:{}".format(__name__, __version__),
    "{}:{}".format(COSMOS_VERSION, JSON_RPC_VERSION),
]

if os.name == "nt":
    _default_user_agent.append(
        "{}:{}".format(os.environ.get("COMPUTERNAME"), os.environ.get("USERNAME"))
    )
else:
    _default_user_agent.append(
        "{}:{}".format(os.environ.get("HOSTNAME"), os.environ.get("USER"))
    )

USER_AGENT = os.environ.get(_user_agent, " ".join(_default_user_agent))
