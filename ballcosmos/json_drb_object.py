# -*- coding: latin-1 -*-

# Copyright 2017 Ball Aerospace & Technologies Corp.
# All Rights Reserved.
#
# This program is free software; you can modify and/or redistribute it
# under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; version 3 with
# attribution addendums as found in the LICENSE.txt

import threading
import socket
import select
import json
import os
import time
import struct
import errno
from ballcosmos.json_rpc import *

class DRbConnError(Exception):
  pass

class JsonDRbObject:
  """Class to perform JSON-RPC Calls to the COSMOS Server (or other JsonDrb server)

  The JsonDRbObject can be used to call COSMOS server methods directly:
    server = JsonDRbObject('127.0.0.1', 7777)
    server.cmd(...)
  """

  def __init__(self, hostname, port, connect_timeout = 1.0):
    """Constructor

    Parameters:
    hostname -- The name of the machine which has started the JSON service
    port -- The port number of the JSON service
    """

    if (str(hostname).upper() == 'LOCALHOST'):
      hostname = '127.0.0.1'

    self.hostname = hostname
    self.port = port
    self.mutex = threading.Lock()
    self.socket = None
    r, w = os.pipe()
    self.pipe_reader = os.fdopen(r)
    self.pipe_writer = os.fdopen(w, 'w')
    self.id = 0
    self.debug = False
    self.request_in_progress = False
    self.connect_timeout = connect_timeout
    if self.connect_timeout != None:
      self.connect_timeout = float(self.connect_timeout)
    self.shutdown_needed = False

  def disconnect(self):
    """Disconnects from the JSON server"""
    self.close_socket()
    self.pipe_writer.write('.')
    # Cannot set @socket to None here because this method can be called by
    # other threads and @socket being None would cause unexpected errors in method_missing
    # Also don't want to take the mutex so that we can interrupt method_missing if necessary
    # Only method_missing can set @socket to None

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
          raise DRbConnError("Shutdown")

        if self.socket == None or self.request_in_progress:
          self.connect()

        response = self.make_request(method_name, method_params, first_try)
        if response == None:
          self.disconnect()
          self.socket = None
          was_first_try = first_try
          first_try = False
          if was_first_try:
            continue

        return self.handle_response(response)

  # private

  def close_socket(self):
    """Close the socket in a manner that ensures that any reads blocked in select will unblock across platforms"""

    if self.socket != None:
      # Calling shutdown and then sleep seems to be required
      # to get select to reliably unblock on linux
      try:
        self.socket.shutdown(SHUT_RDWR)
        time.sleep(0)
      except:
        pass # Oh well we tried

      try:
        self.socket.close()
      except:
        pass # Oh well we tried

  def receive_message(self, data, pipe_reader):
    """Receive a JsonDrb message

    Parameters:
    data -- Bytearray which has already been read from the socket.
    pipe_reader -- Used to break out of select
    return -- The request message
    """

    self.get_at_least_x_bytes_of_data(data, 4, pipe_reader)
    if len(data) >= 4:
      length = struct.unpack('>I', data[0:4])[0]
      data = data[4:]
    else:
      return None

    self.get_at_least_x_bytes_of_data(data, length, pipe_reader)
    if len(data) >= length:
      message = data[0:length]
      data = data[length:]
      return message
    else:
      return None

  def get_at_least_x_bytes_of_data(self, current_data, required_num_bytes, pipe_reader):
    """Reads at least x bytes of data from a socket

    Parameters:
    current_data -- Binary data read from the socket
    required_num_bytes -- The minimum number of bytes to read
    pipe_reader -- Used to break out of select before returning
    """

    while (len(current_data) < required_num_bytes):
      try:
        data = self.socket.recv(65535)
        current_data[len(current_data):] = bytes(data)
      except socket.error as e:
        # IO::WaitReadable
        err = e.args[0]
        if err == errno.EAGAIN or err == errno.EWOULDBLOCK or err == errno.EINPROGRESS:
          select.select([self.socket], [], [])
        else:
          raise e

  def send_data(self, data, send_timeout = 10.0):
    """send data on the socket

    Parameters:
    data -- Binary data to send to the socket
    send_timeout -- The number of seconds to wait for the send to complete
    """

    num_bytes_to_send = len(data) + 4
    total_bytes_sent = 0
    bytes_sent = 0
    data_to_send = struct.pack('>I', len(data))
    data_to_send = bytearray(data_to_send)
    data_to_send[len(data_to_send):] = bytearray(data, encoding='latin-1')

    while True:
      try:
        bytes_sent = self.socket.send(data_to_send[total_bytes_sent:])
      except socket.error as e: # Errno::EAGAIN, Errno::EWOULDBLOCK
        err = e.args[0]
        if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
          result = select.select([], [self.socket], [], send_timeout)
          if len(result[1]) > 0:
            continue
          else:
            raise RuntimeError("Send Timeout")
        else:
          raise e
      total_bytes_sent += bytes_sent
      if total_bytes_sent >= num_bytes_to_send:
        break

    return bytes_sent

  def connect(self):
    if self.request_in_progress:
      self.disconnect()
      self.socket = None
      self.request_in_progress = False

    try:
      self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
      self.socket.setblocking(False)
      r, w = os.pipe()
      self.pipe_reader = os.fdopen(r)
      self.pipe_writer = os.fdopen(w, 'w')

      try:
        self.socket.connect((self.hostname, self.port))
      except socket.error as e:
        err = e.args[0]
        if err == errno.EAGAIN or err == errno.EWOULDBLOCK or err == errno.EINPROGRESS: # IO::WaitWritable
          try:
            result = select.select([], [self.socket], [], self.connect_timeout) # wait 3-way handshake completion
          except Exception as e: # IOError, Errno::ENOTSOCK
            self.disconnect()
            self.socket = None
            raise RuntimeError("Connect canceled 1 : {:s}".format(repr(e)))
          if len(result[1]) > 0:
            while True:
              try:
                self.socket.connect((self.hostname, self.port)) # check connection failure
              except socket.error as e: # Errno::EINPROGRESS
                err = e.args[0]
                if err == errno.EINPROGRESS:
                  continue
                elif err == errno.ENOTSOCK:
                  self.disconnect()
                  self.socket = None
                  raise RuntimeError("Connect canceled ENOTSOCK")
                elif err != errno.EISCONN and err != errno.EALREADY:
                  raise err
              except Exception as e: # IOError, Errno::ENOTSOCK
                self.disconnect()
                self.socket = None
                raise RuntimeError("Connect canceled 2 : {:s}".format(repr(e)))
              break
          else:
            self.disconnect()
            self.socket = None
            raise RuntimeError("Connect timeout")
        else: # IOError, Errno::ENOTSOCK
          self.disconnect()
          self.socket = None
          raise RuntimeError("Connect canceled 4 : errno #{:d}".format(err))
    except Exception as e:
      raise DRbConnError(str(e))

  def make_request(self, method_name, method_params, first_try):
    request = JsonRpcRequest(method_name, method_params, self.id)
    self.id += 1

    hash = convert_bytearray_to_string_raw(request.hash)
    request_data = json.dumps(hash)
    try:
      if self.debug:
        print("Request:")
        print(request_data)
      self.request_in_progress = True
      self.send_data(request_data)
      response_data = self.receive_message(bytearray(), self.pipe_reader)
      self.request_in_progress = False
      if self.debug:
        print("\nResponse:")
        print(response_data)
    except Exception as e:
      self.disconnect()
      self.socket = None
      if first_try:
        return None
      else:
        raise DRbConnError(str(e))
    return response_data

  def handle_response(self, response_data):
    # The code below will always either raise or return breaking out of the loop
    if response_data != None:
      response = JsonRpcResponse.from_json(response_data)
      if isinstance(response, JsonRpcErrorResponse):
        #~ if response.error.data
          #~ raise Exception.from_hash(response.error.data)
        #~ else
        raise RuntimeError("JsonDRb Error ({:d}): {:s}".format(response.error().code(), response.error().message()))
      else:
        return response.result()
    else:
      # Socket was closed by server
      self.disconnect()
      self.socket = None
      raise DRbConnError("Socket closed by server")
