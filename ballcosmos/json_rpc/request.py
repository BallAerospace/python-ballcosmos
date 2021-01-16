#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
json_rpc/request.py
"""
import json

from ballcosmos.environment import (
    COSMOS_VERSION,
    JSON_RPC_VERSION,
)
from ballcosmos.exceptions import BallCosmosRequestError
from ballcosmos.json_rpc.base import JsonRpc


class JsonRpcRequest(JsonRpc):
    """Represents a JSON Remote Procedure Call Request"""

    DANGEROUS_METHODS = ["__send__", "send", "instance_eval", "instance_exec"]

    def __init__(self, id_: int, method_name: str, scope: str, *args):
        """Constructor

        Arguments:
        id_ -- The identifier which will be matched to the response
        method_name -- The name of the method to call
        scope -- The scope
        args -- Array of strings which represent the parameters to send to the method
        """
        super().__init__()
        self["method"] = str(method_name)
        self["params"] = args
        if COSMOS_VERSION != "4":
            self["keyword_params"] = {"scope": scope}
        self["id"] = int(id_)

    @property
    def method(self):
        """Returns the method to call"""
        return self["method"]

    @property
    def params(self):
        """Returns the array of strings which represent the parameters to send to the method"""
        return self.get("params")

    @property
    def keyword_params(self):
        """Returns a dictionary of strings which represent the keyword parameters to send to the method"""
        if COSMOS_VERSION == "4":
            raise RuntimeWarning(
                "invalid version: ({}) keyword_params not allowed".format(
                    COSMOS_VERSION
                )
            )
        return self.get("keyword_params")

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
            hash_["id"],
            hash_["method"],
            hash_.get("keyword_params", {}).get("scope"),
            *hash_.get("params", []),
        )
