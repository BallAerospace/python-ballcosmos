# -*- coding: latin-1 -*-

# Copyright 2017 Ball Aerospace & Technologies Corp.
# All Rights Reserved.
#
# This program is free software; you can modify and/or redistribute it
# under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; version 3 with
# attribution addendums as found in the LICENSE.txt

import json

#~ class Object
  #~ def as_json(options = nil) #:nodoc:
    #~ if respond_to?(:to_hash)
      #~ to_hash
    #~ else
      #~ instance_variables
    #~ end
  #~ end
#~ end

#~ class Struct #:nodoc:
  #~ def as_json(options = nil)
    #~ pairs = []
    #~ self.each_pair { |k, v| pairs << k.to_s; pairs << v.as_json(options) }
    #~ Hash[*pairs]
  #~ end
#~ end

#~ class TrueClass
  #~ def as_json(options = nil) self end #:nodoc:
#~ end

#~ class FalseClass
  #~ def as_json(options = nil) self end #:nodoc:
#~ end

#~ class NilClass
  #~ def as_json(options = nil) self end #:nodoc:
#~ end

#~ class String
  #~ NON_ASCII_PRINTABLE = /[^\x21-\x7e\s]/

  #~ def as_json(options = nil)
    #~ if self =~ NON_ASCII_PRINTABLE
      #~ self.to_json_raw_object
    #~ else
      #~ self
    #~ end
  #~ end #:nodoc:
#~ end

#~ class Symbol
  #~ def as_json(options = nil) to_s end #:nodoc:
#~ end

#~ class Numeric
  #~ def as_json(options = nil) self end #:nodoc:
#~ end

#~ class Regexp
  #~ def as_json(options = nil) to_s end #:nodoc:
#~ end

#~ module Enumerable
  #~ def as_json(options = nil) #:nodoc:
    #~ to_a.as_json(options)
  #~ end
#~ end

#~ class Array
  #~ def as_json(options = nil) #:nodoc:
    #~ map { |v| v.as_json(options) }
  #~ end
#~ end

#~ class Hash
  #~ def as_json(options = nil) #:nodoc:
    #~ pairs = []
    #~ self.each { |k, v| pairs << k.to_s; pairs << v.as_json(options) }
    #~ Hash[*pairs]
  #~ end
#~ end

#~ class Time
  #~ def as_json(options = nil) #:nodoc:
    #~ to_json(options).remove_quotes
  #~ end
#~ end

#~ class Date
  #~ def as_json(options = nil) #:nodoc:
    #~ to_json(options).remove_quotes
  #~ end
#~ end

#~ class DateTime
  #~ def as_json(options = nil) #:nodoc:
    #~ to_json(options).remove_quotes
  #~ end
#~ end

#~ class Exception
  #~ def as_json(*a)
    #~ hash = {}
    #~ hash['class'] = self.class.name
    #~ hash['message'] = self.message
    #~ hash['backtrace'] = self.backtrace
    #~ instance_vars = {}
    #~ self.instance_variables.each do |instance_var_name|
      #~ instance_vars[instance_var_name.to_s] = self.instance_variable_get(instance_var_name.to_s.intern)
    #~ end
    #~ hash['instance_variables'] = instance_vars
    #~ hash.as_json(*a)
  #~ end

  #~ def to_json(*a)
    #~ as_json(*a).to_json(*a)
  #~ end

  #~ def self.from_hash(hash)
    #~ begin
      #~ # Get Error class handling namespaced constants
      #~ split_error_class_name = hash['class'].split("::")
      #~ error_class = Object
      #~ split_error_class_name.each do |name|
        #~ error_class = error_class.const_get(name)
      #~ end
    #~ rescue
      #~ error = Cosmos::JsonDRbUnknownError.new(hash['message'])
      #~ error.set_backtrace(hash['backtrace'].concat(caller()))
      #~ raise error
    #~ end
    #~ error = error_class.new(hash['message'])
    #~ error.set_backtrace(hash['backtrace'].concat(caller())) if hash['backtrace']
    #~ hash['instance_variables'].each do |name, value|
      #~ error.instance_variable_set(name.intern, value)
    #~ end
    #~ error
  #~ end
#~ end

class JsonDRbUnknownError(Exception):
  """An unknown JSON DRb error which can be re-raised by Exception"""
  pass

class JsonRpc:
  """Base class for all JSON Remote Procedure Calls.

  Provides basic comparison and Hash to JSON conversions.
  """

  def __init__(self):
    self.hash = {}

  #~ # @param other [JsonRpc] Another JsonRpc to compare hash values with
  #~ def <=>(other)
    #~ self.as_json <=> other.as_json
  #~ end

  #~ # @param a [Array] Array of options
  #~ # @return [Hash] Hash representing the object
  #~ def as_json(*a)
    #~ @hash.as_json(*a)
  #~ end

  #~ # @param a [Array] Array of options
  #~ # @return [String] The JSON encoded String
  #~ def to_json(*a)
    #~ as_json(*a).to_json(*a)
  #~ end

class JsonRpcRequest(JsonRpc):
  """Represents a JSON Remote Procedure Call Request"""

  DANGEROUS_METHODS = ['__send__', 'send', 'instance_eval', 'instance_exec']

  def __init__(self, method_name, method_params, id):
    """Constructor

    Arguments:
    method_name -- The name of the method to call
    method_params -- Array of strings which represent the parameters to send to the method
    id -- The identifier which will be matched to the response
    """

    JsonRpc.__init__(self)
    self.hash['jsonrpc'] = "2.0"
    self.hash['method'] = str(method_name)
    if method_params != None and len(method_params) != 0:
      self.hash['params'] = method_params
    self.hash['id'] = int(id)

  def method(self):
    """Returns the method to call"""
    return self.hash['method']

  def params(self):
    """Returns the array of strings which represent the parameters to send to the method"""
    try:
      return self.hash['params']
    except KeyError:
      return []

  def id(self):
    """Returns the request identifier"""
    return self.hash['id']

  @classmethod
  def from_json(cls, request_data):
    """Creates and returns a JsonRpcRequest object from a JSON encoded String.

    The version must be 2.0 and the JSON must include the method and id members.

    Parameters:
    request_data -- JSON encoded string representing the request
    """

    try:
      hash = json.loads(request_data)

      # Verify the jsonrpc version is correct and there is a method and id
      if not (hash['jsonrpc'] == "2.0" and 'method' in hash and 'id' in hash):
        raise RuntimeError()
      return cls.from_hash(hash)
    except Exception:
      raise RuntimeError("Invalid JSON-RPC 2.0 Request")

  @classmethod
  def from_hash(cls, hash):
    """Creates a JsonRpcRequest object from a Hash

    Parameters:
    hash -- Hash containing the following keys: method, params, and id
    """
    return cls(hash['method'], hash['params'], hash['id'])

class JsonRpcResponse(JsonRpc):
  """Represents a JSON Remote Procedure Call Response"""

  def __init__(self, id):
    """Constructor

    Parameters:
    id -- The identifier which will be matched to the request
    """

    JsonRpc.__init__(self)
    self.hash['jsonrpc'] = "2.0"
    self.hash['id'] = id

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
      hash = json.loads(response_data)
    except Exception as e:
      raise RuntimeError(msg + " : "  + repr(e))

    # Verify the jsonrpc version is correct and there is an ID
    if not (hash['jsonrpc'] == "2.0" and 'id' in hash):
      raise RuntimeError(msg)

    # If there is a result this is probably a good response
    if 'result' in hash:
      # Can't have an error key in a good response
      if 'error' in hash:
        raise RuntimeError(msg)
      return JsonRpcSuccessResponse.from_hash(hash)
    elif 'error' in hash:
      # There was an error key so create an error response
      return JsonRpcErrorResponse.from_hash(hash)
    else:
      # Neither a result or error key so raise exception
      raise RuntimeError(msg)

def convert_bytearray_to_string_raw(object):
  if isinstance(object, (bytes, bytearray)):
    return object.decode('latin-1')
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

def convert_string_raw_to_bytearray(object):
  if isinstance(object, dict):
    try:
      json_class = object['json_class']
      raw = object['raw']
      return bytearray(raw)
    except Exception as e:
      for key, value in object.items():
        object[key] = convert_string_raw_to_bytearray(value)
      return object
  elif isinstance(object, (tuple, list)):
    object = list(object)
    index = 0
    for value in object:
      object[index] = convert_string_raw_to_bytearray(value)
      index += 1
    return object
  else:
    return object

class JsonRpcSuccessResponse(JsonRpcResponse):
  """Represents a JSON Remote Procedure Call Success Response"""

  def __init__(self, result, id):
    """Constructor

    Parameters:
    id -- The identifier which will be matched to the request
    """

    JsonRpcResponse.__init__(self, id)
    result = convert_string_raw_to_bytearray(result)
    self.hash['result'] = result

  def result(self):
    """"Return the result of the method request"""
    return self.hash['result']

  @classmethod
  def from_hash(cls, hash):
    """Creates a JsonRpcSuccessResponse object from a Hash

    Parameters
    hash -- Hash containing the following keys: result and id
    """
    return cls(hash['result'], hash['id'])

class JsonRpcErrorResponse(JsonRpcResponse):
  """Represents a JSON Remote Procedure Call Error Response"""

  def __init__(self, error, id):
    """Constructor

    Parameters:
    error -- The error object
    id -- The identifier which will be matched to the request
    """

    JsonRpcResponse.__init__(self, id)
    self.hash['error'] = error

  def error(self):
    """Returns the error object"""
    return self.hash['error']

  @classmethod
  def from_hash(cls, hash):
    """Creates a JsonRpcErrorResponse object from a Hash

    Parameters:
    hash -- Hash containing the following keys: error and id
    """
    return cls(JsonRpcError.from_hash(hash['error']), hash['id'])

class JsonRpcError(JsonRpc):
  """Represents a JSON Remote Procedure Call Error"""

  def __init__(self, code, message, data = None):
    """Constructor

    Parameters:
    code -- The error type that occurred
    message -- A short description of the error
    data -- Additional information about the error
    """

    JsonRpc.__init__(self)
    self.hash['code'] = code
    self.hash['message'] = message
    self.hash['data'] = data

  def code(self):
    """Returns the error type that occurred"""
    return self.hash['code']

  def message(self):
    """Returns a short description of the error"""
    return self.hash['message']

  def data(self):
    """Returns additional information about the error"""
    return self.hash['data']

  @classmethod
  def from_hash(cls, hash):
    """Creates a JsonRpcError object from a Hash

    Parameters:
    hash -- Hash containing the following keys: code, message, and optionally data
    """
    if 'code' in hash and (int(hash['code']) == hash['code']) and 'message' in hash:
      return cls(hash['code'], hash['message'], hash['data'])
    else:
      raise RuntimeError("Invalid JSON-RPC 2.0 Error")
