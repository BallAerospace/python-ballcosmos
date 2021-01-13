#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
test_drb.py
"""

import unittest
from unittest.mock import patch, MagicMock

from ballcosmos.exceptions import (
    BallCosmosRequestError,
    BallCosmosResponseError
)
from ballcosmos.json_drb_object import JsonDRbObject


class TestDrbObject(unittest.TestCase):

    HOST, PORT = "127.0.0.1", 7777

    @patch("ballcosmos.json_drb_object.HTTPConnection.connect")
    def test_object(self, connect):
        """
        Test json request
        """
        connect.return_value = 'test'
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
        mock.getresponse.return_value.read.return_value = b'{"jsonrpc": "2.0", "id": 107, "result": 0}'
        connection.return_value = mock
        cmd_tlm_server = JsonDRbObject(self.HOST, self.PORT)
        cmd_tlm_server.write("test")
        self.assertIsNotNone(cmd_tlm_server.connection)


if __name__ == '__main__':
    unittest.main()
