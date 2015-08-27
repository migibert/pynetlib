from __future__ import absolute_import
import mock
import unittest
from pynetlib.utils import execute_command, find_values_or_default_value
from pynetlib.namespace import Namespace
from nose_parameterized import parameterized


class TestUtils(unittest.TestCase):

    @mock.patch('pynetlib.utils.subprocess.check_output')
    def test_execute_command(self, check_output):
        execute_command('command arg1 arg2')
        check_output.assert_called_once_with('command arg1 arg2', shell=True)

    @mock.patch('pynetlib.utils.subprocess.check_output')
    def test_execute_command_in_namespace(self, check_output):
        namespace = Namespace('namespace')
        execute_command('command arg1 arg2', namespace=namespace)
        check_output.assert_called_once_with('ip netns exec namespace command arg1 arg2', shell=True)

    @mock.patch('pynetlib.utils.subprocess.check_output')
    def test_execute_command_in_default_namespace(self, check_output):
        namespace = Namespace(Namespace.DEFAULT_NAMESPACE_NAME)
        execute_command('command arg1 arg2', namespace=namespace)
        check_output.assert_called_once_with('command arg1 arg2', shell=True)

    @mock.patch('pynetlib.utils.subprocess.check_output')
    def test_execute_command_in_string_namespace(self, check_output):
        namespace = 'namespace'
        execute_command('command arg1 arg2', namespace=namespace)
        check_output.assert_called_once_with('ip netns exec namespace command arg1 arg2', shell=True)

    def test_find_values(self):
        values = 'key value'
        value = find_values_or_default_value(values, 'key', single=True)
        self.assertEqual(value, 'value')

    @parameterized.expand([
        ('key value', 'key', True, None, 'value'),
        ('', 'test', True, 'value', 'value'),
        ('key', 'key', True, None, None),
        ('key', 'key', True, 'test', 'test'),
        ('key value1 key value2', 'key', False, None, ['value1', 'value2'])
    ])
    def test_find_values_or_default_value(self, values, key, single, default, expected):
        value = find_values_or_default_value(values, key, single=single, default_value=default)
        self.assertEqual(value, expected)
