#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
test_json_rpc.py
"""

import unittest

from ballcosmos.exceptions import BallCosmosRequestError, BallCosmosResponseError
from ballcosmos.json_rpc.request import JsonRpcRequest
from ballcosmos.json_rpc.response import JsonRpcResponse


class TestJsonRpc(unittest.TestCase):
    def test_basic_request(self):
        """
        Test json request
        """
        json_request_example = '{"jsonrpc": "2.0", "method": "connect_interface", "params": ["EXAMPLE_INT"], "id": 110}'
        request = JsonRpcRequest.from_json(json_request_example)
        self.assertEqual(request.json_rpc, "2.0")
        self.assertIsNotNone(request.id)

    def test_bad_request(self):
        """
        Test json request
        """
        json_request_example = (
            '{"method": "connect_interface", "params": ["EXAMPLE_INT"], "id": 110}'
        )
        with self.assertRaises(BallCosmosRequestError) as context:
            JsonRpcRequest.from_json(json_request_example)
            self.assertTrue("jsonrpc" in context.exception)

    def test_basic_response(self):
        """
        Test json response
        """
        json_response_example = b'{"jsonrpc": "2.0", "id": 107, "result": 0}'
        request = JsonRpcResponse.from_json(json_response_example)
        self.assertEqual(request.json_rpc, "2.0")
        self.assertIsNotNone(request.id)
        self.assertEqual(request.result, 0)

    def test_bad_response(self):
        """
        Test json response
        """
        json_response_example = b'{"id": 107, "result": 0}'
        with self.assertRaises(BallCosmosResponseError) as context:
            JsonRpcResponse.from_json(json_response_example)
            self.assertTrue("jsonrpc" in context.exception)


if __name__ == "__main__":
    unittest.main()
