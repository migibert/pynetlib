import mock
import unittest
from pynetlib.utils import execute_command, find_value
from pynetlib.models import Namespace
from pynetlib.exceptions import ValueNotFoundException


class TestNamespace(unittest.TestCase):

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

    def test_find_value(self):
        values = ['key', 'value']
        value = find_value(values, 'key')
        self.assertEqual(value, 'value')

    def test_find_non_existing_key(self):
        values = ['key', 'value']
        value = find_value(values, 'test')
        self.assertIsNone(value)

    def test_find_non_existing_value(self):
        values = ['key']
        with self.assertRaises(ValueNotFoundException):
            find_value(values, 'key')

    def test_find_two_values(self):
        values = ['key', 'value', 'key', 'other']
        value = find_value(values, 'key')
        self.assertEqual(value, 'value')


if __name__ == '__main__':
    unittest.main()
