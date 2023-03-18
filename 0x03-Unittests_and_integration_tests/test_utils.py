#!/usr/bin/env python3
"""
a python unit test for utils files
"""
import unittest
import requests
from unittest.mock import patch
from utils import access_nested_map, get_json, memoize
from parameterized import parameterized


class TestAccessNestedMap(unittest.TestCase):
    """a class for testing access nested map method"""

    @parameterized.expand([
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2)
        ])
    def test_access_nested_map(self, nst_map, key, result):
        """
        test_access_nested_map - a method to test access nested map function
        Arguments:
            nst_map: the given nested map
            key: the key value to search for nested map
        Returns:
            the value found in the nested map
        """
        self.assertEqual(access_nested_map(nst_map, key), result)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nst_map, key):
        """
        test_access_nested_map_exception - method to test the exception
        rguments:
            nst_map: the given nested map
            key: the key value to search for nested map
        Returns:
            the value found in the nested map
        """
        with self.assertRaises(Exception) as err:
            access_nested_map(nst_map, key)


class TestGetJson(unittest.TestCase):
    """a class to test the get json method"""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, url, payload):
        """
        test_get_json - function to test the get json method
        Arguments:
            url: the given url that we need to test
            payload: the expected output
        Returns:
            ok if is succes else fail
        """
        with patch('requests.get') as mk_rqst:
            mk_rqst.return_value.json.return_value = payload
            self.assertEqual(get_json(url), payload)


class TestMemoize(unittest.TestCase):
    """a classs to test memoize function"""
    def test_memoize(self):
        """
        test_memoize: function to test the memoize method of utils
        Arguments:
            nothing
        Returns:
            ok if it succedd else fail
        """
        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mk:
            tst = TestClass()
            tst.a_property()
            tst.a_property()
            mk.assert_called_once()
