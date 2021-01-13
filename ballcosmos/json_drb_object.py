#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
json_drb_object.py
"""

# Copyright 2017 Ball Aerospace & Technologies Corp.
# All Rights Reserved.
#
# This program is free software; you can modify and/or redistribute it
# under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; version 3 with
# attribution addendums as found in the LICENSE.txt

import time
import json
from http.client import HTTPConnection
from threading import RLock
from contextlib import ContextDecorator

from ballcosmos.environment import MAX_RETRY_COUNT, X_CSRF_TOKEN
from ballcosmos.exceptions import (
    BallCosmosConnectionError,
    BallCosmosRequestError,
    BallCosmosResponseError,
)
from ballcosmos.json_rpc import (
    JsonRpcRequest,
    JsonRpcResponse,
    JsonRpcErrorResponse,
    convert_bytearray_to_string_raw,
)


class JsonDRbObject(ContextDecorator):
    """Class to perform JSON-RPC Calls to the COSMOS Server (or other JsonDrb server)

    The JsonDRbObject can be used to call COSMOS server methods directly:
      server = JsonDRbObject('127.0.0.1', 7777)
      server.cmd(...)
      or
      with JsonDRbObject('127.0.0.1', 7777) as server:
        server.cmd(...)
    """

    def __init__(self, hostname: str, port: int, connect_timeout: float = 1.0):
        """Constructor

        Parameters:
        hostname -- The name of the machine which has started the JSON service
        port -- The port number of the JSON service
        """
        if str(hostname).upper() == "LOCALHOST":
            hostname = "127.0.0.1"
        self.timeout = None
        self.hostname = hostname
        self.port = port
        self.mutex = RLock()
        self.connection = None
        self.socket = None
        self.id = 0
        self.debug = False
        self.request_in_progress = False
        self.connect_timeout = connect_timeout
        if self.connect_timeout is not None:
            self.connect_timeout = float(self.connect_timeout)
        self.shutdown_needed = False

    def __enter__(self):
        if self.shutdown_needed:
            raise BallCosmosConnectionError(
                "Shutdown needed: {}".format(self.shutdown_needed)
            )

        if self.connection is None or self.request_in_progress:
            self._connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is not None:
                pass
                # f'Exception during thread execution: {exc_type} {exc_val}'
        finally:
            self.disconnect()
        return False

    def disconnect(self):
        """Disconnects from the JSON server"""
        if self.connection:
            self.connection.close()
        # Cannot set @connection to None here because this method can be called by
        # other threads and @connection being None would cause unexpected errors in method_missing
        # Also don't want to take the mutex so that we can interrupt method_missing if necessary
        # Only method_missing can set @connection to None

    def shutdown(self):
        """Permanently disconnects from the JSON server"""
        self.shutdown_needed = True
        self.disconnect()

    def write(self, method_name, *method_params):
        """Forwards all method calls to the remote service.

        method_name -- Name of the method to call
        method_params -- Array of parameters to pass to the method
        return -- The result of the method call. If the method raises an exception
          the same exception is also raised. If something goes wrong with the
          protocol a DRb::DRbConnError exception is raised.
        """

        with self.mutex:
            # This flag and loop are used to automatically reconnect and retry if something goes
            # wrong on the first attempt writing to the socket.   Sockets can become disconnected
            # between function calls, but as long as the remote server is back up and running the
            # call should succeed even when it discovers a broken socket on the first attempt.
            first_try = True
            while True:
                if self.shutdown_needed:
                    raise BallCosmosConnectionError(
                        "Shutdown needed: {}".format(self.shutdown_needed)
                    )

                if self.connection is None or self.request_in_progress:
                    self._connect()

                response = self._make_request(method_name, method_params, first_try)
                if response is None:
                    self.disconnect()
                    self.connection = None
                    was_first_try = first_try
                    first_try = False
                    if was_first_try:
                        continue

                return self._handle_response(response)

    def _connect(self):
        if self.request_in_progress:
            self.disconnect()
            self.connection = None
            self.request_in_progress = False

        exception_ = None
        for i in range(MAX_RETRY_COUNT):
            try:
                if self.debug:
                    print("connect try {} out of {}".format(i, MAX_RETRY_COUNT))

                self.connection = HTTPConnection(self.hostname, self.port)
                self.timeout = self.connect_timeout
                self.connection.connect()

            except ConnectionRefusedError as e:
                exception_ = e
                time.sleep(1)
            except ConnectionError as e:
                exception_ = e
                break
            except Exception as e:
                exception_ = e
                break

        if exception_ is not None:
            if self.debug:
                print("connect failed {}".format(exception_))
            self.disconnect()
            self.connection = None
            raise BallCosmosConnectionError(
                "failed to connection to cosmos"
            ) from exception_

    def _make_request(self, method_name, method_params, first_try):
        request = JsonRpcRequest(method_name, method_params, self.id)
        self.id += 1

        hash_ = convert_bytearray_to_string_raw(request)
        request_data = json.dumps(hash_)
        try:
            if self.debug:
                print("Request:\n{}".format(request_data))
            self.request_in_progress = True
            self.connection.request(
                method="POST",
                url="/",
                body=request_data,
                headers={
                    "Content-Type": "application/json-rpc",
                    "X_CSRF_TOKEN": X_CSRF_TOKEN,
                },
            )
            response = self.connection.getresponse()
            response_data = response.read()
            self.request_in_progress = False
            if self.debug:
                print("Response:\n{}".format(response_data))
        except Exception as e:
            self.disconnect()
            self.connection = None
            if first_try:
                return None
            else:
                raise BallCosmosRequestError(
                    "failed to make request: {}".format(request)
                ) from e
        return response_data

    def _handle_response(self, response_data):
        # The code below will always either raise or return breaking out of the loop
        if response_data is None:
            # Socket was closed by server
            self.disconnect()
            self.socket = None
            raise BallCosmosResponseError("socket closed by server")

        response = JsonRpcResponse.from_json(response_data)
        if self.debug:
            print("response:\n{}".format(response))
        try:
            return response.result
        except AttributeError:
            msg = "id {}, error code: {}, message: {}".format(
                response.id, response.error.code, response.error.message
            )
            raise RuntimeError(msg, response)
