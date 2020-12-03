#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
json_rpc/__init__.py
"""

from ballcosmos.json_rpc.error import JsonRpcError
from ballcosmos.json_rpc.request import JsonRpcRequest
from ballcosmos.json_rpc.response import (
    JsonRpcResponse,
    JsonRpcErrorResponse,
    JsonRpcSuccessResponse,
    convert_bytearray_to_string_raw,
    convert_json_class,
)


class JsonRpc(dict):
    """Base class for all JSON Remote Procedure Calls.

    Provides basic comparison and Hash to JSON conversions.
    """

    @property
    def id(self):
        return self.get("id")

    @property
    def json_rpc(self):
        return self.get("jsonrpc", "2.0")
