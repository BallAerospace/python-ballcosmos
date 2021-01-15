#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
json_rpc/request.py
"""
import json

from ballcosmos.environment import JSON_RPC_VERSION, COSMOS_VERSION
from ballcosmos.exceptions import BallCosmosRequestError
from ballcosmos.json_rpc.base import JsonRpc


class JsonRpcRequest(JsonRpc):
    """Represents a JSON Remote Procedure Call Request"""

    DANGEROUS_METHODS = ["__send__", "send", "instance_eval", "instance_exec"]

    def __init__(self, method_name, method_params, id_, keyword_params=None):
        """Constructor

        Arguments:
        method_name -- The name of the method to call
        method_params -- Array of strings which represent the parameters to send to the method
        id_ -- The identifier which will be matched to the response
        keyword_params -- Dict of key, value strings which represent the keyword parameters to send to the method
        """
        super().__init__()
        self["method"] = str(method_name)
        if method_params is not None and len(method_params) != 0:
            self["params"] = method_params
        if COSMOS_VERSION != "4":
            self["keyword_params"] = {"scope": "DEFAULT"}
            if keyword_params is not None:
                self["keyword_params"].update(keyword_params)
        self["id"] = int(id_)

    @property
    def method(self):
        """Returns the method to call"""
        return self["method"]

    @property
    def params(self):
        """Returns the array of strings which represent the parameters to send to the method"""
        try:
            return self["params"]
        except KeyError:
            return []

    @property
    def keyword_params(self):
        """Returns a dictonary of strings which represent the keyword parameters to send to the method"""
        if COSMOS_VERSION == "4":
            raise RuntimeWarning(
                "invalid version: ({}) keyword_params not allowed".format(
                    COSMOS_VERSION
                )
            )
        try:
            return self["keyword_params"]
        except KeyError:
            return {"scope": "*"}

    @property
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
        msg = "invaid json-rpc {} request".format(JSON_RPC_VERSION)
        try:
            hash_ = json.loads(request_data)
            # Verify the jsonrpc version is correct and there is a method and id
            if hash_["jsonrpc"] != JSON_RPC_VERSION:
                raise ValueError("message jsonrpc version: {}".format(hash_["jsonrpc"]))
            return cls.from_hash(hash_)
        except (ValueError, KeyError) as e:
            raise BallCosmosRequestError(msg) from e
        except Exception as e:
            raise RuntimeError(msg) from e

    @classmethod
    def from_hash(cls, hash_):
        """Creates a JsonRpcRequest object from a Hash

        Parameters:
        hash_ -- Hash containing the following keys: method, params, id, and keyword_params
        """
        return cls(
            hash_["method"], hash_["params"], hash_["id"], hash_.get("keyword_params")
        )
