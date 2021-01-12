#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
environment.py
"""

import os

_json_rpc_version = "COSMOS_JSON_RPC_VERSION"

_x_csrf_token = "COSMOS_X_CSRF_TOKEN"

_max_retry_count = "COSMOS_MAX_RETRY_COUNT"

JSON_RPC_VERSION = os.environ.get(_x_csrf_token, "2.0")

X_CSRF_TOKEN = os.environ.get(_x_csrf_token, "SuperSecret")

try:
    MAX_RETRY_COUNT = int(os.environ.get(_max_retry_count))
except TypeError:
    MAX_RETRY_COUNT = 3
