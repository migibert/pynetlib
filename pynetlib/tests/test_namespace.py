from mock.mock import call
import mock
import unittest
from . import read_file
from nose_parameterized import parameterized
from pynetlib.exceptions import ObjectAlreadyExistsException, ObjectNotFoundException, ForbiddenException
from pynetlib.namespace import Namespace


class TestNamespace(unittest.TestCase):

    def setUp(self):
        self.ip_addr_list_output = read_file('ip_addr_list')
        self.ip_netns_list_output = read_file('ip_netns_list')

    @parameterized.expand([('mynamespace', False), ('', True)])
    def test_init(self, name, is_default):
        ns = Namespace(name)
        self.assertEqual(ns.name, name)
        self.assertEqual(len(ns.devices), 0)
        self.assertEqual(ns.is_default(), is_default)

    def test_equality(self):
        name = 'namespace'
        ns1 = Namespace(name)
        ns2 = Namespace(name)
        self.assertEqual(ns1, ns2)

    @mock.patch('pynetlib.namespace.execute_command')
    def test_namespace_discovery(self, execute_command):

        execute_command.return_value = self.ip_netns_list_output
        default_namespace = Namespace('')
        first_namespace = Namespace('first_namespace')
        second_namespace = Namespace('second_namespace')

        namespaces = Namespace.discover()

        self.assertEqual(len(namespaces), 3)
        self.assertTrue(default_namespace in namespaces)
        self.assertTrue(first_namespace in namespaces)
        self.assertTrue(second_namespace in namespaces)

    @mock.patch('pynetlib.namespace.execute_command')
    def test_namespace_creation(self, execute_command):
        namespace = Namespace('namespace')
        namespace.create()
        self.assertTrue(execute_command.call_count, 2)
        self.assertTrue(call('ip netns list') in execute_command.mock_calls)
        self.assertTrue(call('ip netns add namespace') in execute_command.mock_calls)

    @mock.patch('pynetlib.namespace.execute_command')
    def test_default_namespace_creation(self, execute_command):
        namespace = Namespace(Namespace.DEFAULT_NAMESPACE_NAME)
        with self.assertRaises(ObjectAlreadyExistsException):
            namespace.create()
        execute_command.assert_not_called()

    @mock.patch('pynetlib.namespace.execute_command')
    def test_existing_namespace_creation(self, execute_command):
        execute_command.side_effect = ['namespace']
        namespace = Namespace('namespace')
        with self.assertRaises(ObjectAlreadyExistsException):
            namespace.create()
        execute_command.assert_called_once_with('ip netns list')

    @mock.patch('pynetlib.namespace.execute_command')
    def test_namespace_deletion(self, execute_command):
        execute_command.side_effect = ['namespace', None]
        namespace = Namespace('namespace')
        namespace.delete()
        self.assertTrue(execute_command.call_count, 2)
        self.assertTrue(call('ip netns list') in execute_command.mock_calls)
        self.assertTrue(call('ip netns del namespace') in execute_command.mock_calls)

    @mock.patch('pynetlib.namespace.execute_command')
    def test_default_namespace_deletion(self, execute_command):
        execute_command.side_effect = ['']
        namespace = Namespace(Namespace.DEFAULT_NAMESPACE_NAME)
        with self.assertRaises(ForbiddenException):
            namespace.delete()
        execute_command.assert_not_called()

    @mock.patch('pynetlib.namespace.execute_command')
    def test_non_existing_namespace_deletion(self, execute_command):
        namespace = Namespace('namespace')
        with self.assertRaises(ObjectNotFoundException):
            namespace.delete()
        execute_command.assert_called_once_with('ip netns list')

    @mock.patch('pynetlib.namespace.execute_command')
    def test_namespace_existence(self, execute_command):
        execute_command.side_effect = ['namespace']
        namespace = Namespace('namespace')
        result = namespace.exists()
        self.assertTrue(result)
        execute_command.assert_called_once_with('ip netns list')

    @mock.patch('pynetlib.namespace.execute_command')
    def test_default_namespace_existence(self, execute_command):
        namespace = Namespace(Namespace.DEFAULT_NAMESPACE_NAME)
        result = namespace.exists()
        self.assertTrue(result)
        execute_command.assert_called_once_with('ip netns list')

    @mock.patch('pynetlib.namespace.execute_command')
    def test_non_existing_namespace_existence(self, execute_command):
        namespace = Namespace('namespace')
        result = namespace.exists()
        self.assertFalse(result)
        execute_command.assert_called_once_with('ip netns list')


if __name__ == '__main__':
    unittest.main()
