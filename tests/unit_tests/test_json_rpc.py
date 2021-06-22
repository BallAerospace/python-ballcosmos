#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
test_json_rpc_error.py
"""

import unittest

from ballcosmos.json_rpc import (
    JsonRpcError,
    JsonRpcRequest,
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
        self.assertIsNotNone(response)
        self.assertEqual(response.result(), 0)

    def test_advanced_byte_response(self):
        """
        Test json response
        """
        json_response_example = {
            "jsonrpc": "2.0",
            "id": 13,
            "result": {
                "foo": bytearray(b"\x00\x01\xcaj\x01\x81`\x00\xe4\xe3\x00\t"),
            },
        }
        response = JsonRpcSuccessResponse.from_hash(json_response_example)
        self.assertIsNotNone(response)
        self.assertNotEqual(response.result(), 0)

    def test_advanced_response(self):
        """
        Test json response
        """
        json_response_example = {
            "jsonrpc": "2.0",
            "id": 13,
            "result": [
                {"json_class": "Float", "raw": "Infinity"},
                {"json_class": "Float", "raw": "-Infinity"},
                {"json_class": "Float", "raw": "NaN"},
            ],
        }
        response = JsonRpcSuccessResponse.from_hash(json_response_example)
        self.assertIsNotNone(response)
        self.assertNotEqual(response.result(), 0)

    def test_bad_response_missing_version(self):
        """
        Test json response
        """
        json_response_example = b'{"id": 107, "result": 0}'
        with self.assertRaises(KeyError) as context:
            JsonRpcResponse.from_json(json_response_example)
            self.assertTrue("jsonrpc" in context.exception)

    def test_bad_response_missing_id(self):
        """
        Test json response
        """
        json_response_example = b'{"jsonrpc": "1.0", "result": {}}'
        with self.assertRaises(RuntimeError) as context:
            JsonRpcResponse.from_json(json_response_example)
            self.assertTrue("jsonrpc" in context.exception)

    def test_bad_response_version(self):
        """
        Test json response
        """
        json_response_example = b'{"jsonrpc": "1.0", "id": 107, "result": 0}'
        with self.assertRaises(RuntimeError) as context:
            JsonRpcResponse.from_json(json_response_example)
            self.assertTrue("jsonrpc" in context.exception)

    def test_error_response(self):
        """
        Test json response
        """
        json_response_example = {
            "jsonrpc": "2.0",
            "id": 107,
            "error": {"code": 1234, "message": "foobar", "data": {"foo": "bar"}},
        }
        response = JsonRpcErrorResponse.from_hash(json_response_example)
        self.assertIsNotNone(response.error())

    def test_bad_json(self):
        """
        Test json request
        """
        json_response_example = b"foobar"
        with self.assertRaises(Exception) as context:
            JsonRpcResponse.from_json(json_response_example)
            self.assertTrue("msg" in context.exception)

    # TestJsonRpcError

    def test_error(self):
        """
        Test json request
        """
        json_request_example = {"code": 1234, "message": "foobar", "data": {}}
        request = JsonRpcError.from_hash(json_request_example)
        print(request.code())
        self.assertEqual(request.code(), 1234)
        self.assertIsNotNone(request.message())
        self.assertIsNotNone(request.data())

    def test_bad_error(self):
        """
        Test json request
        """
        json_request_example = {"message": "foobar", "data": {}}
        with self.assertRaises(RuntimeError) as context:
            JsonRpcError.from_hash(json_request_example)
            self.assertTrue("Invalid" in context.exception)

    # TestJsonRpc

    def test_basic_5_request(self):
        """
        Test json request
        """
        json_request_example = """
            {
                "jsonrpc": "2.0",
                "method": "connect_interface",
                "params": ["EXAMPLE_INT"],
                "id": 110
            }
        """
        request = JsonRpcRequest.from_json(json_request_example)
        self.assertIsNotNone(request.id())
        self.assertIsNotNone(request.method())
        self.assertIsNotNone(request.params())

    def test_basic_4_request(self):
        """
        Test json request
        """
        json_request_example = """
            {
                "jsonrpc": "2.0",
                "method": "connect_interface",
                "params": ["EXAMPLE_INT"],
                "id": 110
            }
        """
        request = JsonRpcRequest.from_json(json_request_example)
        self.assertIsNotNone(request.id())
        self.assertIsNotNone(request.method())
        self.assertIsNotNone(request.params())

    def test_bad_json_rpc_version(self):
        """
        Test json request
        """
        json_request_example = '{"jsonrpc": "1.0", "method": "connect_interface", "params": ["EXAMPLE_INT"]}'
        with self.assertRaises(RuntimeError) as context:
            JsonRpcRequest.from_json(json_request_example)
            self.assertTrue("jsonrpc" in context.exception)

    def test_bad_request(self):
        """
        Test json request
        """
        json_request_example = (
            '{"method": "connect_interface", "params": ["EXAMPLE_INT"], "id": 110}'
        )
        with self.assertRaises(RuntimeError) as context:
            JsonRpcRequest.from_json(json_request_example)
            self.assertTrue("jsonrpc" in context.exception)


if __name__ == "__main__":
    unittest.main()
