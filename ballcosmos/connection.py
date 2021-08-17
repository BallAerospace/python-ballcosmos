#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
connection.py
"""

# Copyright 2021 Ball Aerospace & Technologies Corp.
# All Rights Reserved.
#
# This program is free software; you can modify and/or redistribute it
# under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; version 3 with
# attribution addendums as found in the LICENSE.txt


import json
import time
import logging
from http.client import HTTPConnection
from threading import RLock, Event

from ballcosmos.__version__ import __title__
from ballcosmos.json_rpc import *
from ballcosmos.environment import (
  COSMOS_TOKEN,
  LOG_LEVEL,
  MAX_RETRY_COUNT,
)

logger = logging.getLogger(__title__)
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    level=logging.getLevelName(LOG_LEVEL),
)

class ConnectionError(RuntimeError):
  pass

class Connection:
  """Class to perform JSON-RPC Calls to the COSMOS Server (or other JsonDrb server)

  The Connection can be used to call COSMOS server methods directly:
    server = Connection('127.0.0.1', 7777)
    server.cmd(...)
  """

  def __init__(self, hostname, port, connect_timeout = 1.0):
    """Constructor

    Parameters:
    hostname -- The name of the machine which has started the JSON service
    port -- The port number of the JSON service
    """
    self.id = 0
    self._x_csrf_token = COSMOS_TOKEN
    self.hostname = '127.0.0.1' if str(hostname).upper() == 'LOCALHOST' else hostname
    self.port = port
    self.mutex = RLock()
    self.connection = None
    self.connect_timeout = connect_timeout
    if self.connect_timeout is not None:
      self.connect_timeout = float(self.connect_timeout)
    self.request_in_progress = Event()
    self.shutdown_needed = Event()

  def disconnect(self):
    """Disconnects from the JSON server"""
    if (self.connection):
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
      protocol a Connection.ConnectionError exception is raised.
    """

    with self.mutex:
      # This flag and loop are used to automatically reconnect and retry if something goes
      # wrong on the first attempt writing to the socket.   Sockets can become disconnected
      # between function calls, but as long as the remote server is back up and running the
      # call should succeed even when it discovers a broken socket on the first attempt.
      first_try = True
      while True:
        if self.shutdown_needed.is_set():
          raise ConnectionError("Shutdown")

        if self.connection is None or self.request_in_progress.is_set():
          self.connect()

        response = self.make_request(method_name, method_params, first_try)
        if response is None:
          self.disconnect()
          self.connection = None
          if first_try:
            first_try = False
            continue

        return self.handle_response(response)

  # private
  def connect(self):
    if self.request_in_progress.is_set():
      self.disconnect()
      self.connection = None
      self.request_in_progress.clear()

    exception_ = None
    for i in range(MAX_RETRY_COUNT):
        logger.debug("connect try %d out of %d", i, MAX_RETRY_COUNT)
        try:
            self.connection = HTTPConnection(
                self.hostname,
                self.port,
                timeout=self.connect_timeout,
            )
            self.connection.connect()
            logger.debug("connected on try %d out of %d", i, MAX_RETRY_COUNT)
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
        self.connection = None
        raise RuntimeError(
          f"Failed to connect to COSMOS on {self.hostname}:{self.port}"
        ) from exception_

  def make_request(self, method_name, method_params, first_try):
    request = JsonRpcRequest(method_name, method_params, self.id)
    self.id += 1
    hash_ = convert_bytearray_to_string_raw(request.hash)
    request_kwargs = {
        "method": "POST",
        "url": "/",
        "body": json.dumps(hash_),
        "headers": {
            "Content-Type": "application/json-rpc",
            "X_CSRF_TOKEN": self._x_csrf_token
        },
    }
    try:
      logger.debug("request: %s", request_kwargs)
      self.request_in_progress.set()
      self.connection.request(**request_kwargs)
      response_data = self.connection.getresponse().read()
      self.request_in_progress.clear()
      logger.debug("response: %s", response_data)
    except Exception as e:
      self.disconnect()
      self.connection = None
      if first_try:
        return None
      else:
        raise ConnectionError(f"failed to make request: {request}") from e
    return response_data

  def handle_response(self, response_data):
    # The code below will always either raise or return breaking out of the loop
    if response_data != None:
      response = JsonRpcResponse.from_json(response_data)
      if isinstance(response, JsonRpcErrorResponse):
        #~ if response.error.data
          #~ raise Exception.from_hash(response.error.data)
        #~ else
        raise RuntimeError(f"Connection error {response}")
      else:
        return response.result()
    else:
      # Socket was closed by server
      self.disconnect()
      self.socket = None
      raise ConnectionError("Socket closed by server")
