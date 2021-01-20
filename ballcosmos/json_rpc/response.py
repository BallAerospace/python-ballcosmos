#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
json_rpc/response.py
"""
import json

from ballcosmos.environment import JSON_RPC_VERSION
from ballcosmos.exceptions import BallCosmosResponseError
from ballcosmos.json_rpc.base import JsonRpc
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
    def from_json(cls, response_data: bytes):
        """Creates a JsonRpcResponse object from a JSON encoded String.

        The version must be 2.0 and the JSON must include the id members. It must also
        include either result for success or error for failure but never both.

        Parameters:
        response_data -- JSON encoded string representing the response
        """

        msg = "invalid json-rpc {} response".format(JSON_RPC_VERSION)
        try:
            hash_ = json.loads(response_data.decode("latin-1"))
        except Exception as e:
            raise RuntimeError(msg, response_data) from e

        try:
            # Verify the jsonrpc version is correct and there is an ID
            if hash_["jsonrpc"] != JSON_RPC_VERSION:
                raise BallCosmosResponseError(msg)
        except KeyError as e:
            raise BallCosmosResponseError(msg, response_data) from e

        try:
            return JsonRpcErrorResponse.from_hash(hash_)
        except KeyError:
            pass

        try:
            return JsonRpcSuccessResponse.from_hash(hash_)
        except KeyError:
            pass

        raise BallCosmosResponseError(msg, response_data)


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
        except Exception:
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

    def __init__(self, id_, result):
        """Constructor

        Parameters:
        id -- The identifier which will be matched to the request
        result -- The result of the request
        """
        super().__init__(id_)
        result = convert_json_class(result)
        self["result"] = result

    @property
    def result(self):
        """"Return the result of the method request"""
        return self["result"]

    @classmethod
    def from_hash(cls, hash_):
        """Creates a JsonRpcSuccessResponse object from a Hash

        Parameters
        hash_ -- Hash containing the following keys: result and id
        """
        return cls(hash_["id"], hash_["result"])


class JsonRpcErrorResponse(JsonRpcResponse):
    """Represents a JSON Remote Procedure Call Error Response"""

    def __init__(self, id_, error):
        """Constructor

        Parameters:
        id -- The identifier which will be matched to the request
        error -- The error object
        """
        super().__init__(id_)
        self["error"] = JsonRpcError.from_hash(error)

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
        return cls(hash_["id"], hash_["error"])
