#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
json_rpc/request.py
"""
import json

from ballcosmos.json_rpc import JsonRpc


class JsonRpcRequest(JsonRpc):
    """Represents a JSON Remote Procedure Call Request"""

    DANGEROUS_METHODS = ["__send__", "send", "instance_eval", "instance_exec"]

    def __init__(self, method_name, method_params, id_):
        """Constructor

        Arguments:
        method_name -- The name of the method to call
        method_params -- Array of strings which represent the parameters to send to the method
        id_ -- The identifier which will be matched to the response
        """
        super().__init__()
        self["method"] = str(method_name)
        if method_params is not None and len(method_params) != 0:
            self["params"] = method_params
        self["id"] = int(id_)

    def method(self):
        """Returns the method to call"""
        return self["method"]

    def params(self):
        """Returns the array of strings which represent the parameters to send to the method"""
        try:
            return self["params"]
        except KeyError:
            return []

    def id(self):
        """Returns the request identifier"""
        return self["id"]

    @classmethod
    def from_json(cls, request_data):
        """Creates and returns a JsonRpcRequest object from a JSON encoded String.

        The version must be 2.0 and the JSON must include the method and id members.

        Parameters:
        request_data -- JSON encoded string representing the request
        """

        try:
            hash_ = json.loads(request_data)

            # Verify the jsonrpc version is correct and there is a method and id
            if not (hash_["jsonrpc"] == "2.0" and "method" in hash_ and "id" in hash_):
                raise RuntimeError()
            return cls.from_hash(hash_)
        except Exception:
            raise RuntimeError("Invalid JSON-RPC 2.0 Request")

    @classmethod
    def from_hash(cls, hash_):
        """Creates a JsonRpcRequest object from a Hash

        Parameters:
        hash_ -- Hash containing the following keys: method, params, and id
        """
        return cls(hash_["method"], hash_["params"], hash_["id"])
