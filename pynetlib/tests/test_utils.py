from __future__ import absolute_import
import mock
import unittest
from pynetlib.utils import execute_command, find_values_or_default_value
from pynetlib.namespace import Namespace
from pynetlib.exceptions import ValueNotFoundException


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

    def test_find_values_non_existing_key(self):
        values = 'key value'
        value = find_values_or_default_value(values, 'test', single=True)
        self.assertIsNone(value)

    def test_find_values_non_existing_value(self):
        values = 'key'
        value = find_values_or_default_value(values, 'key', single=True)
        self.assertIsNone(value)

    def test_find_values_two_values(self):
        values = 'key value key other'
        values = find_values_or_default_value(values, 'key')
        self.assertEqual(len(values), 2)
        self.assertTrue('value' in values)
        self.assertTrue('other' in values)


if __name__ == '__main__':
    unittest.main()
