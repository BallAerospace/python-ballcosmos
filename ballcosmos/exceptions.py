#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
exceptions.py
"""

# Copyright 2021 Ball Aerospace & Technologies Corp.
# All Rights Reserved.
#
# This program is free software; you can modify and/or redistribute it
# under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; version 3 with
# attribution addendums as found in the LICENSE.txt

from ballcosmos.json_rpc import *


class CosmosError(RuntimeError):
    pass


class CosmosConnectionError(CosmosError):
    pass


class CosmosRetryError(CosmosError):
    pass


class CosmosRequestError(CosmosError):
    def __init__(self, message: str, request: JsonRpcRequest):
        super().__init__(message, request)
        self.request = request


class CosmosResponseError(CosmosError):
    def __init__(self, request: JsonRpcRequest, response: JsonRpcErrorResponse):
        super().__init__(request, response)
        self.request = request
        self.response = response
