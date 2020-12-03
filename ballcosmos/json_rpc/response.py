#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
json_rpc/response.py
"""
import json

from ballcosmos.json_rpc import JsonRpc
from ballcosmos.json_rpc.error import JsonRpcError


class JsonRpcResponse(JsonRpc):
    """Represents a JSON Remote Procedure Call Response"""

    def __init__(self, id_):
        """Constructor

        Parameters:
        id -- The identifier which will be matched to the request
        """
        super().__init__()
        self["id"] = id_

    @classmethod
    def from_json(cls, response_data):
        """Creates a JsonRpcResponse object from a JSON encoded String.

        The version must be 2.0 and the JSON must include the id members. It must also
        include either result for success or error for failure but never both.

        Parameters:
        response_data -- JSON encoded string representing the response
        """

        msg = "Invalid JSON-RPC 2.0 Response"
        try:
            hash_ = json.loads(response_data.decode("latin-1"))
        except Exception as e:
            raise RuntimeError(msg + " : " + repr(e))

        # Verify the jsonrpc version is correct and there is an ID
        if not (hash_["jsonrpc"] == "2.0" and "id" in hash_):
            raise RuntimeError(msg)

        # If there is a result this is probably a good response
        if "result" in hash_:
            # Can't have an error key in a good response
            if "error" in hash_:
                raise RuntimeError(msg)
            return JsonRpcSuccessResponse.from_hash(hash_)
        elif "error" in hash_:
            # There was an error key so create an error response
            return JsonRpcErrorResponse.from_hash(hash_)
        else:
            # Neither a result or error key so raise exception
            raise RuntimeError(msg)


def convert_bytearray_to_string_raw(object_):
    if isinstance(object_, (bytes, bytearray)):
        return object_.decode("latin-1")
    elif isinstance(object_, dict):
        for key, value in object_.items():
            object_[key] = convert_bytearray_to_string_raw(value)
        return object_
    elif isinstance(object_, (tuple, list)):
        object_ = list(object_)
        index = 0
        for value in object_:
            object_[index] = convert_bytearray_to_string_raw(value)
            index += 1
        return object_
    else:
        return object_


def convert_json_class(object_):
    if isinstance(object_, dict):
        try:
            json_class = object_["json_class"]
            raw = object_["raw"]
            if json_class == "Float":
                if raw == "Infinity":
                    return float("inf")
                elif raw == "-Infinity":
                    return -float("inf")
                elif raw == "NaN":
                    return float("nan")
                else:
                    return raw
            else:
                return bytearray(raw)
        except Exception as e:
            for key, value in object_.items():
                object_[key] = convert_json_class(value)
            return object_
    elif isinstance(object_, (tuple, list)):
        object_ = list(object_)
        index = 0
        for value in object_:
            object_[index] = convert_json_class(value)
            index += 1
        return object_
    else:
        return object_


class JsonRpcSuccessResponse(JsonRpcResponse):
    """Represents a JSON Remote Procedure Call Success Response"""

    def __init__(self, result, id_):
        """Constructor

        Parameters:
        id -- The identifier which will be matched to the request
        """

        JsonRpcResponse.__init__(self, id_)
        result = convert_json_class(result)
        self["result"] = result

    def result(self):
        """"Return the result of the method request"""
        return self["result"]

    @classmethod
    def from_hash(cls, hash_):
        """Creates a JsonRpcSuccessResponse object from a Hash

        Parameters
        hash_ -- Hash containing the following keys: result and id
        """
        return cls(hash_["result"], hash_["id"])


class JsonRpcErrorResponse(JsonRpcResponse):
    """Represents a JSON Remote Procedure Call Error Response"""

    def __init__(self, error, id_):
        """Constructor

        Parameters:
        error -- The error object
        id -- The identifier which will be matched to the request
        """

        JsonRpcResponse.__init__(self, id_)
        self["error"] = error

    @property
    def error(self):
        """Returns the error object"""
        return self["error"]

    @classmethod
    def from_hash(cls, hash_):
        """Creates a JsonRpcErrorResponse object from a Hash

        Parameters:
        hash -- Hash containing the following keys: error and id
        """
        return cls(JsonRpcError.from_hash(hash_["error"]), hash_["id"])
