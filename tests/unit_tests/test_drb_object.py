#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
test_drb_object.py
"""

import unittest
from unittest.mock import patch, MagicMock

from ballcosmos.exceptions import BallCosmosRequestError, BallCosmosResponseError
from ballcosmos.json_drb_object import JsonDRbObject


class TestDrbObject(unittest.TestCase):

    HOST, PORT = "127.0.0.1", 7777

    @patch("ballcosmos.json_drb_object.HTTPConnection.connect")
    def test_object(self, connect):
        """
        Test json request
        """
        connect.return_value = "test"
        cmd_tlm_server = JsonDRbObject(self.HOST, self.PORT)
        self.assertIsNone(cmd_tlm_server.connection)

    @patch("ballcosmos.json_drb_object.HTTPConnection")
    def test_connection(self, connection):
        """
        Test connection
        """
        mock = MagicMock()
        mock.connect.return_value = MagicMock()
        mock.request.request = MagicMock()
        mock.getresponse.return_value.read.return_value = (
            b'{"jsonrpc": "2.0", "id": 107, "result": 0}'
        )
        connection.return_value = mock
        cmd_tlm_server = JsonDRbObject(self.HOST, self.PORT)
        cmd_tlm_server.write("test")
        self.assertIsNotNone(cmd_tlm_server.connection)
        mock.connect.assert_called_once()
        mock.request.assert_called_once()

    @patch("ballcosmos.json_drb_object.HTTPConnection")
    def test_with_connection(self, connection):
        """
        Test connection
        """
        mock = MagicMock()
        mock.connect.return_value = MagicMock()
        mock.request.request = MagicMock()
        mock.getresponse.return_value.read.return_value = (
            b'{"jsonrpc": "2.0", "id": 107, "result": 0}'
        )
        connection.return_value = mock
        with JsonDRbObject(self.HOST, self.PORT) as cmd_tlm_server:
            cmd_tlm_server.write("test")
            self.assertIsNotNone(cmd_tlm_server.connection)
        mock.connect.assert_called_once()
        mock.request.assert_called_once()

    @patch("ballcosmos.json_drb_object.time.sleep")
    @patch("ballcosmos.json_drb_object.HTTPConnection")
    def test_connection_refused_error(self, connection, sleep):
        """
        Test connection
        """
        sleep.return_value = None
        mock = MagicMock()
        mock.connect.side_effect = ConnectionRefusedError("test")
        connection.return_value = mock
        cmd_tlm_server = JsonDRbObject(self.HOST, self.PORT)
        with self.assertRaises(RuntimeError):
            cmd_tlm_server.write("test")
        self.assertIsNone(cmd_tlm_server.connection)
        mock.connect.assert_called()
        mock.request.assert_not_called()

    @patch("ballcosmos.json_drb_object.HTTPConnection")
    def test_connection_error(self, connection):
        """
        Test connection
        """
        mock = MagicMock()
        mock.connect.side_effect = ConnectionError("test")
        connection.return_value = mock
        cmd_tlm_server = JsonDRbObject(self.HOST, self.PORT)
        with self.assertRaises(RuntimeError):
            cmd_tlm_server.write("test")
        self.assertIsNone(cmd_tlm_server.connection)
        mock.connect.assert_called_once()
        mock.request.assert_not_called()

    @patch("ballcosmos.json_drb_object.HTTPConnection")
    def test_response_none(self, connection):
        """
        Test connection
        """
        mock = MagicMock()
        mock.connect.return_value = MagicMock()
        mock.request.request = MagicMock()
        mock.getresponse.return_value.read.return_value = None
        connection.return_value = mock
        cmd_tlm_server = JsonDRbObject(self.HOST, self.PORT)
        with self.assertRaises(RuntimeError):
            cmd_tlm_server.write("test")
        self.assertIsNone(cmd_tlm_server.connection)
        mock.connect.assert_called()
        mock.request.assert_called()

    @patch("ballcosmos.json_drb_object.HTTPConnection")
    def test_response_error(self, connection):
        """
        Test connection
        """
        mock = MagicMock()
        mock.connect.return_value = MagicMock()
        mock.request.request = MagicMock()
        mock.getresponse.side_effect = ConnectionResetError("test")
        connection.return_value = mock
        cmd_tlm_server = JsonDRbObject(self.HOST, self.PORT)
        with self.assertRaises(RuntimeError):
            cmd_tlm_server.write("test")
        self.assertIsNone(cmd_tlm_server.connection)
        mock.connect.assert_called()
        mock.request.assert_called()

    @patch("ballcosmos.json_drb_object.HTTPConnection")
    def test_response_result_error(self, connection):
        """
        Test connection
        """
        mock = MagicMock()
        mock.connect.return_value = MagicMock()
        mock.request.request = MagicMock()
        mock.getresponse.return_value.read.return_value = b"""
            {
                "jsonrpc": "2.0",
                "id": 107,
                "error": {
                    "code": "1234",
                    "message": "foobar",
                    "data": {
                        "foo": "bar"
                    }
                }
            }
        """
        connection.return_value = mock
        cmd_tlm_server = JsonDRbObject(self.HOST, self.PORT)
        response = cmd_tlm_server.write("test")
        self.assertIsNotNone(response)
        mock.connect.assert_called_once()
        mock.request.assert_called_once()

    @patch("ballcosmos.json_drb_object.HTTPConnection")
    def test_response_result_invalid(self, connection):
        """
        Test connection
        """
        mock = MagicMock()
        mock.connect.return_value = MagicMock()
        mock.request.request = MagicMock()
        mock.getresponse.return_value.read.return_value = (
            b'{"jsonrpc": "2.0", "id": 107}'
        )
        connection.return_value = mock
        cmd_tlm_server = JsonDRbObject(self.HOST, self.PORT)
        with self.assertRaises(RuntimeError) as context:
            cmd_tlm_server.write("test")
            print(context)
        self.assertIsNotNone(cmd_tlm_server.connection)
        mock.connect.assert_called_once()
        mock.request.assert_called_once()


if __name__ == "__main__":
    unittest.main()
