#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
environment.py
"""

import os

from ballcosmos import __name__, __version__


_cosmos_version = "COSMOS_VERSION"

_user_agent = "COSMOS_USER_AGENT"

_json_rpc_version = "COSMOS_JSON_RPC_VERSION"

_x_csrf_token = "COSMOS_X_CSRF_TOKEN"

_max_retry_count = "COSMOS_MAX_RETRY_COUNT"

COSMOS_VERSION = os.environ.get(_cosmos_version, "5")

JSON_RPC_VERSION = os.environ.get(_json_rpc_version, "2.0")

_default_user_agent = [
    "{}:{}".format(__name__, __version__),
    "{}:{}".format(COSMOS_VERSION, JSON_RPC_VERSION),
]

if os.name == "nt":
    _default_user_agent.append(
        "{}:{}".format(os.environ.get("COMPUTERNAME"), os.environ.get("USERNAME")),
    )
else:
    _default_user_agent.append(
        "{}:{}".format(os.environ.get("HOSTNAME"), os.environ.get("USER")),
    )

USER_AGENT = os.environ.get(_user_agent, " ".join(_default_user_agent))

X_CSRF_TOKEN = os.environ.get(_x_csrf_token, "SuperSecret")

try:
    MAX_RETRY_COUNT = int(os.environ.get(_max_retry_count))
except TypeError:
    MAX_RETRY_COUNT = 3
