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

from ballcosmos.__version__ import __title__, __version__

_cosmos_token = "COSMOS_X_CSRF_TOKEN"

_default_cts_hostname = "COSMOS_CTS_HOSTNAME"

_default_replay_hostname = "COSMOS_REPLAY_HOSTNAME"

_default_cts_port = "COSMOS_CTS_PORT"

_default_replay_port = "COSMOS_REPLAY_PORT"

_log_level = "COSMOS_LOG_LEVEL"

_max_retry_count = "COSMOS_MAX_RETRY_COUNT"

COSMOS_TOKEN = os.environ.get(_cosmos_token, "SuperSecret")

DEFAULT_CTS_API_HOST = os.environ.get(_default_cts_hostname, "127.0.0.1")

DEFAULT_REPLAY_API_HOST = os.environ.get(_default_replay_hostname, "127.0.0.1")

try:
    DEFAULT_CTS_API_PORT = int(os.environ.get(_default_cts_port))
except TypeError:
    DEFAULT_CTS_API_PORT = 7777

try:
    DEFAULT_REPLAY_API_PORT = int(os.environ.get(_default_replay_port))
except TypeError:
    DEFAULT_REPLAY_API_PORT = 7877

LOG_LEVEL = os.environ.get(_log_level, "INFO")

try:
    MAX_RETRY_COUNT = int(os.environ.get(_max_retry_count))
except TypeError:
    MAX_RETRY_COUNT = 3
