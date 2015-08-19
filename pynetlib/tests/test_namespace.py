from mock.mock import call
import os
import mock
import unittest
from nose_parameterized import parameterized
from pynetlib.exceptions import ObjectAlreadyExistsException, ObjectNotFoundException, ForbiddenException
from pynetlib.models import Namespace, Device

IP_ADDR_RESULT = os.path.join(os.path.dirname(__file__) + '/fixtures', 'ip_addr_list')
IP_NETNS_RESULT = os.path.join(os.path.dirname(__file__) + '/fixtures', 'ip_netns_list')


class TestNamespace(unittest.TestCase):

    def setUp(self):
        self.ip_addr_list_output = open(IP_ADDR_RESULT).read()
        self.ip_netns_list_output = open(IP_NETNS_RESULT).read()

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

    @mock.patch('pynetlib.models.execute_command')
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

    @mock.patch('pynetlib.models.execute_command')
    def test_device_discovery(self, execute_command):

        execute_command.side_effect = [
            self.ip_netns_list_output,
            self.ip_addr_list_output,
            self.ip_addr_list_output,
            self.ip_addr_list_output
        ]
        lo = Device('1', 'lo')
        lo.inet = ['127.0.0.1/8']
        lo.inet6 = ['::1/128']
        eth0 = Device('2', 'eth0')
        eth0.inet = ['10.0.2.15/24', '10.0.2.16/24']
        eth0.inet6 = ['fe80::a00:27ff:feea:67cf/64']
        docker0 = Device('3', 'docker0')
        docker0.inet = ['172.17.42.1/16']
        docker0.inet6 = []

        namespaces = Namespace.discover(with_devices=True)

        self.assertEqual(len(namespaces), 3)
        for namespace in namespaces:
            self.assertEqual(len(namespace.devices), 3)
            self.assertTrue(lo in namespace.devices)
            self.assertTrue(eth0 in namespace.devices)
            self.assertTrue(docker0 in namespace.devices)

    @mock.patch('pynetlib.models.execute_command')
    def test_namespace_creation(self, execute_command):
        namespace = Namespace('namespace')
        namespace.create()
        self.assertTrue(execute_command.call_count, 2)
        self.assertTrue(call('ip netns list') in execute_command.mock_calls)
        self.assertTrue(call('ip netns add namespace') in execute_command.mock_calls)

    @mock.patch('pynetlib.models.execute_command')
    def test_default_namespace_creation(self, execute_command):
        namespace = Namespace(Namespace.DEFAULT_NAMESPACE_NAME)
        with self.assertRaises(ObjectAlreadyExistsException):
            namespace.create()
        execute_command.assert_not_called()

    @mock.patch('pynetlib.models.execute_command')
    def test_existing_namespace_creation(self, execute_command):
        execute_command.side_effect = ['namespace']
        namespace = Namespace('namespace')
        with self.assertRaises(ObjectAlreadyExistsException):
            namespace.create()
        execute_command.assert_called_once_with('ip netns list')

    @mock.patch('pynetlib.models.execute_command')
    def test_namespace_deletion(self, execute_command):
        execute_command.side_effect = ['namespace', None]
        namespace = Namespace('namespace')
        namespace.delete()
        self.assertTrue(execute_command.call_count, 2)
        self.assertTrue(call('ip netns list') in execute_command.mock_calls)
        self.assertTrue(call('ip netns del namespace') in execute_command.mock_calls)

    @mock.patch('pynetlib.models.execute_command')
    def test_default_namespace_deletion(self, execute_command):
        execute_command.side_effect = ['']
        namespace = Namespace(Namespace.DEFAULT_NAMESPACE_NAME)
        with self.assertRaises(ForbiddenException):
            namespace.delete()
        execute_command.assert_not_called()

    @mock.patch('pynetlib.models.execute_command')
    def test_non_existing_namespace_deletion(self, execute_command):
        namespace = Namespace('namespace')
        with self.assertRaises(ObjectNotFoundException):
            namespace.delete()
        execute_command.assert_called_once_with('ip netns list')

    @mock.patch('pynetlib.models.execute_command')
    def test_namespace_existence(self, execute_command):
        execute_command.side_effect = ['namespace']
        namespace = Namespace('namespace')
        result = namespace.exists()
        self.assertTrue(result)
        execute_command.assert_called_once_with('ip netns list')

    @mock.patch('pynetlib.models.execute_command')
    def test_default_namespace_existence(self, execute_command):
        namespace = Namespace(Namespace.DEFAULT_NAMESPACE_NAME)
        result = namespace.exists()
        self.assertTrue(result)
        execute_command.assert_called_once_with('ip netns list')

    @mock.patch('pynetlib.models.execute_command')
    def test_non_existing_namespace_existence(self, execute_command):
        namespace = Namespace('namespace')
        result = namespace.exists()
        self.assertFalse(result)
        execute_command.assert_called_once_with('ip netns list')


if __name__ == '__main__':
    unittest.main()
