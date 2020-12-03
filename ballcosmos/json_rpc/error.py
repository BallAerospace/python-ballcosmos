#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
json_rpc/error.py
"""

from ballcosmos.json_rpc import JsonRpc


class JsonRpcError(JsonRpc):
    """Represents a JSON Remote Procedure Call Error"""

    def __init__(self, code, message, data=None):
        """Constructor

        Parameters:
        code -- The error type that occurred
        message -- A short description of the error
        data -- Additional information about the error
        """
        super().__init__()
        self["code"] = code
        self["message"] = message
        self["data"] = data

    @property
    def code(self):
        """Returns the error type that occurred"""
        return self.get("code")

    @property
    def message(self):
        """Returns a short description of the error"""
        return self.get("message")

    @property
    def data(self):
        """Returns additional information about the error"""
        return self.get("data")

    @classmethod
    def from_hash(cls, hash_):
        """Creates a JsonRpcError object from a Hash

        Parameters:
        hash -- Hash containing the following keys: code, message, and optionally data
        """
        if (
            "code" in hash_
            and (int(hash_["code"]) == hash_["code"])
            and "message" in hash_
        ):
            return cls(hash_["code"], hash_["message"], hash_["data"])
        else:
            # should be a ValueError
            raise RuntimeError("Invalid JSON-RPC 2.0 Error")
