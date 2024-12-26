import unittest
from unittest import mock
from unittest.mock import Mock, MagicMock
from unittest.mock import patch

import mysql
from mysql.connector import CMySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

import version4.HEPaS_server_2 as db


class MyTestCase(unittest.TestCase):

    @mock.patch.object(CMySQLConnection, "cursor")
    def test_retrieve_user_fail(self, mock_cursor: MagicMock):
        mock_cursor().fetchone.return_value = None
        actual = db.retrieve_user_from_table("12345678", "John", "AAAAAAAAAAAA", "email@example.com")
        self.assertEqual(actual,False)
        self.assertEqual(mock_cursor().fetchone.call_count, 1)

    @mock.patch.object(CMySQLConnection, "cursor")
    def test_get_existing_record_fail(self, mock_cursor: MagicMock):
        mock_cursor().fetchall.return_value = None
        actual = db.get_existing_records("20240514")
        expected = "No records found."
        self.assertEqual(actual, expected)




if __name__ == '__main__':
    unittest.main()