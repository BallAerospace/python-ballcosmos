#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
json_rpc.py"""

# Copyright 2021 Ball Aerospace & Technologies Corp.
# All Rights Reserved.
#
# This program is free software; you can modify and/or redistribute it
# under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; version 3 with
# attribution addendums as found in the LICENSE.txt

import json


class JsonDRbUnknownError(Exception):
    """An unknown JSON DRb error which can be re-raised by Exception"""


class JsonRpc:
    """Base class for all JSON Remote Procedure Calls.

    Provides basic comparison and Hash to JSON conversions.
    """

    def __init__(self):
        self.hash = {}

    def __str__(self):
        return str(self.hash)

    def __repr__(self):
        return str(self.hash)


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
        self.hash["jsonrpc"] = "2.0"
        self.hash["method"] = str(method_name)
        if method_params is not None and len(method_params) != 0:
            self.hash["params"] = method_params
        self.hash["id"] = int(id_)

    def method(self):
        """Returns the method to call"""
        return self.hash["method"]

    def params(self):
        """Returns the array of strings which represent the parameters to send to the method"""
        try:
            return self.hash["params"]
        except KeyError:
            return []

    def id(self):
        """Returns the request identifier"""
        return self.hash["id"]

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


class JsonRpcResponse(JsonRpc):
    """Represents a JSON Remote Procedure Call Response"""

    def __init__(self, id):
        """Constructor

        Parameters:
        id -- The identifier which will be matched to the request
        """

        super().__init__()
        self.hash["jsonrpc"] = "2.0"
        self.hash["id"] = id

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
        except Exception as error:
            raise RuntimeError(f"{msg} : {error}")

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


def convert_bytearray_to_string_raw(object):
    if isinstance(object, (bytes, bytearray)):
        return object.decode("latin-1")
    elif isinstance(object, dict):
        for key, value in object.items():
            object[key] = convert_bytearray_to_string_raw(value)
        return object
    elif isinstance(object, (tuple, list)):
        object = list(object)
        index = 0
        for value in object:
            object[index] = convert_bytearray_to_string_raw(value)
            index += 1
        return object
    else:
        return object


def convert_json_class(object):
    if isinstance(object, dict):
        try:
            json_class = object["json_class"]
            raw = object["raw"]
            if json_class == "Float":
                if raw == "Infinity":
                    return float("inf")
                elif raw == "-Infinity":
                    return -float("inf")
                elif raw == "NaN":
                    return float("nan")
                return raw
            else:
                return bytearray(raw)
        except Exception as error:
            for key, value in object.items():
                object[key] = convert_json_class(value)
            return object
    elif isinstance(object, (tuple, list)):
        object = list(object)
        index = 0
        for value in object:
            object[index] = convert_json_class(value)
            index += 1
        return object
    else:
        return object


class JsonRpcSuccessResponse(JsonRpcResponse):
    """Represents a JSON Remote Procedure Call Success Response"""

    def __init__(self, result, id_):
        """Constructor

        Parameters:
        result -- The result
        id_ -- The identifier which will be matched to the request
        """

        super().__init__(id_)
        result = convert_json_class(result)
        self.hash["result"] = result

    def result(self):
        """ "Return the result of the method request"""
        return self.hash["result"]

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
        id_ -- The identifier which will be matched to the request
        """

        super().__init__(id_)
        self.hash["error"] = error

    def error(self):
        """Returns the error object"""
        return self.hash["error"]

    @classmethod
    def from_hash(cls, hash_):
        """Creates a JsonRpcErrorResponse object from a Hash

        Parameters:
        hash_ -- Hash containing the following keys: error and id
        """
        return cls(JsonRpcError.from_hash(hash_["error"]), hash_["id"])


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
        self.hash["code"] = code
        self.hash["message"] = message
        self.hash["data"] = data

    def code(self):
        """Returns the error type that occurred"""
        return self.hash["code"]

    def message(self):
        """Returns a short description of the error"""
        return self.hash["message"]

    def data(self):
        """Returns additional information about the error"""
        return self.hash["data"]

    @classmethod
    def from_hash(cls, hash_):
        """Creates a JsonRpcError object from a Hash

        Parameters:
        hash_ -- Hash containing the following keys: code, message, and optionally data
        """
        if (
            "code" in hash_
            and (int(hash_["code"]) == hash_["code"])
            and "message" in hash_
        ):
            return cls(hash_["code"], hash_["message"], hash_["data"])
        raise RuntimeError("Invalid JSON-RPC 2.0 Error")
