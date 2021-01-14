#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
test_json_rpc_response.py
"""

import unittest

from ballcosmos.exceptions import BallCosmosResponseError
from ballcosmos.json_rpc.response import (
    JsonRpcResponse,
    JsonRpcSuccessResponse,
    JsonRpcErrorResponse,
)


class TestJsonRpc(unittest.TestCase):
    def test_basic_response(self):
        """
        Test json response
        """
        json_response_example = b'{"jsonrpc": "2.0", "id": 107, "result": 0}'
        response = JsonRpcResponse.from_json(json_response_example)
        self.assertEqual(response.json_rpc, "2.0")
        self.assertIsNotNone(response.id)
        self.assertEqual(response.result, 0)

    def test_bad_response_missing_version(self):
        """
        Test json response
        """
        json_response_example = b'{"id": 107, "result": 0}'
        with self.assertRaises(BallCosmosResponseError) as context:
            JsonRpcResponse.from_json(json_response_example)
            self.assertTrue("jsonrpc" in context.exception)

    def test_bad_response_missing_id(self):
        """
        Test json response
        """
        json_response_example = b'{"jsonrpc": "1.0", "result": {}}'
        with self.assertRaises(BallCosmosResponseError) as context:
            JsonRpcResponse.from_json(json_response_example)
            self.assertTrue("jsonrpc" in context.exception)

    def test_bad_response_version(self):
        """
        Test json response
        """
        json_response_example = b'{"jsonrpc": "1.0", "id": 107, "result": 0}'
        with self.assertRaises(BallCosmosResponseError) as context:
            JsonRpcResponse.from_json(json_response_example)
            self.assertTrue("jsonrpc" in context.exception)

    def test_error_response(self):
        """
        Test json response
        """
        json_response_example = {
            "jsonrpc": "2.0",
            "id": 107,
            "error": {
                "code": "1234",
                "message": "foobar",
                "data": {"foo": "bar"},
            },
        }
        response = JsonRpcErrorResponse.from_hash(json_response_example)
        self.assertEqual(response.json_rpc, "2.0")
        self.assertIsNotNone(response.id)
        self.assertIsNotNone(response.error)
        self.assertIsNotNone(response.error.code)

    def test_bad_json(self):
        """
        Test json request
        """
        json_response_example = b"foobar"
        with self.assertRaises(Exception) as context:
            JsonRpcResponse.from_json(json_response_example)
            self.assertTrue("msg" in context.exception)


if __name__ == "__main__":
    unittest.main()
