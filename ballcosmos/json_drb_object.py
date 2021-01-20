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
import logging
from http.client import HTTPConnection
from threading import RLock, Event
from contextlib import ContextDecorator

from ballcosmos import __title__
from ballcosmos.environment import (
    COSMOS_VERSION,
    COSMOS_SCOPE,
    LOG_LEVEL,
    MAX_RETRY_COUNT,
    USER_AGENT,
    X_CSRF_TOKEN,
)
from ballcosmos.exceptions import BallCosmosConnectionError
from ballcosmos.json_rpc import (
    JsonRpcRequest,
    JsonRpcResponse,
    convert_bytearray_to_string_raw,
)

logger = logging.getLogger(__title__)
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    level=logging.getLevelName(LOG_LEVEL),
)


class JsonDRbObject(ContextDecorator):
    """Class to perform JSON-RPC Calls to the COSMOS Server (or other JsonDrb server)

    The JsonDRbObject can be used to call COSMOS server methods directly:
      server = JsonDRbObject("127.0.0.1", 7777)
      server.cmd(...)
      or
      with JsonDRbObject("127.0.0.1", 7777) as server:
        server.cmd(...)
    """

    def __init__(
        self, hostname: str, port: int, timeout: float = 5.0, scope: str = COSMOS_SCOPE
    ):
        """Constructor

        Parameters:
        hostname -- The name of the machine which has started the JSON service
        port -- The port number of the JSON service
        timeout -- The amount of time the socket will read until an error
        scope -- The scope or project the connection will add to the request
        """
        self.id = 0
        self.scope = scope
        self.timeout = float(timeout)
        self.hostname = hostname if hostname.upper() != "LOCALHOST" else "127.0.0.1"
        self.port = port
        self._mutex = RLock()
        self._connection = None
        self._shutdown_needed = Event()
        self.api_url = "/" if COSMOS_VERSION == "4" else "/api"

    def __enter__(self):
        if self._shutdown_needed.is_set():
            raise BallCosmosConnectionError(
                "Shutdown needed: {}".format(self._shutdown_needed)
            )

        if self._connection is None:
            self._connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is not None:
                pass
                # f'Exception during thread execution: {exc_type} {exc_val}'
        finally:
            self.disconnect()
            self._connection = None
        return False

    def disconnect(self):
        """Disconnects from the JSON server"""
        if self._connection:
            self._connection.close()
        # Cannot set @connection to None here because this method can be called by
        # other threads and @connection being None would cause unexpected errors in method_missing
        # Also don't want to take the mutex so that we can interrupt method_missing if necessary
        # Only method_missing can set @connection to None

    def shutdown(self):
        """Permanently disconnects from the JSON server"""
        self._shutdown_needed.set()
        self.disconnect()

    def write(self, method_name, *args):
        """Forwards all method calls to the remote service.

        method_name -- Name of the method to call
        args -- Array of parameters to pass to the method
        return -- The result of the method call. If the method raises an exception
          the same exception is also raised. If something goes wrong with the
          protocol a DRb::DRbConnError exception is raised.
        """
        with self._mutex:
            # This flag and loop are used to automatically reconnect and retry if something goes
            # wrong on the first attempt writing to the socket.   Sockets can become disconnected
            # between function calls, but as long as the remote server is back up and running the
            # call should succeed even when it discovers a broken socket on the first attempt.
            request = JsonRpcRequest(self.id, method_name, self.scope, *args)
            self.id += 1
            while True:
                logger.debug("write try for request %s", request)
                if self._shutdown_needed.is_set():
                    raise BallCosmosConnectionError(
                        "shutdown needed event: {}".format(
                            self._shutdown_needed.is_set()
                        )
                    )
                if self._connection is None:
                    self._connect()
                try:
                    response = self._make_request(request)
                    return self._handle_response(response)
                except BallCosmosConnectionError:
                    self.disconnect()
                    self._connection = None
                time.sleep(1)

    def _connect(self):
        exception_ = None
        for i in range(MAX_RETRY_COUNT):
            logger.debug("connect try %d out of %d", i, MAX_RETRY_COUNT)
            try:
                self._connection = HTTPConnection(
                    self.hostname,
                    self.port,
                    timeout=self.timeout,
                )
                self._connection.connect()
                exception_ = None
                break
            except ConnectionRefusedError as e:
                exception_ = e
                time.sleep(1)
            except OSError as e:
                exception_ = e
                break

        if exception_ is not None:
            logger.debug("connect failed %s", exception_)
            self.disconnect()
            self._connection = None
            raise BallCosmosConnectionError(
                "failed to connection to cosmos"
            ) from exception_

    def _make_request(self, request: dict):
        hash_ = convert_bytearray_to_string_raw(request)
        request_kwargs = {
            "method": "POST",
            "url": self.api_url,
            "body": json.dumps(hash_),
            "headers": {
                "User-Agent": USER_AGENT,
                "Content-Type": "application/json-rpc",
                "X_CSRF_TOKEN": X_CSRF_TOKEN,
            },
        }
        logger.debug("request: %s", request_kwargs)
        try:
            self._connection.request(**request_kwargs)
            response_data = self._connection.getresponse().read()
            logger.debug("response: %s", response_data)
            return response_data
        except OSError as e:
            raise BallCosmosConnectionError(
                "failed to make request: {}".format(request)
            ) from e

    @staticmethod
    def _handle_response(response_data: bytes):
        # The code below will always either raise or return breaking out of the loop
        response = JsonRpcResponse.from_json(response_data)
        logger.debug("response %s %s", type(response), response)
        try:
            return response.result
        except AttributeError:
            return response
