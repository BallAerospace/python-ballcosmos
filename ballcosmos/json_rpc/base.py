#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
json_rpc/__init__.py
"""

from ballcosmos.environment import JSON_RPC_VERSION


class JsonRpc(dict):
    """Base class for all JSON Remote Procedure Calls.

    Provides basic comparison and Hash to JSON conversions.
    """

    def __init__(self):
        super().__init__()
        self["jsonrpc"] = JSON_RPC_VERSION

    @property
    def id(self):
        return self.get("id")

    @property
    def json_rpc(self):
        return self.get("jsonrpc", JSON_RPC_VERSION)
