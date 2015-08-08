import os
import mock
import unittest
from pynet.models import Namespace, Device

IP_ADDR_RESULT = os.path.join(os.path.dirname(__file__) + '/fixtures', 'ip_addr_list')
IP_NETNS_RESULT = os.path.join(os.path.dirname(__file__) + '/fixtures', 'ip_netns_list')

class TestNamespace(unittest.TestCase):

    def setUp(self):
        self.ip_addr_list_output = open(IP_ADDR_RESULT).read()
        self.ip_netns_list_output = open(IP_NETNS_RESULT).read()

    def test_init(self):
        name = 'mynamespace'
        ns = Namespace(name)
        self.assertEqual(ns.name, name)
        self.assertEqual(len(ns.devices), 0)
        self.assertFalse(ns.is_default())

    def test_init_default(self):
        name = ''
        ns = Namespace(name)
        self.assertEqual(ns.name, name)
        self.assertEqual(len(ns.devices), 0)
        self.assertTrue(ns.is_default())

    def test_equality(self):
        name = 'test'
        id = 'id'
        dev = Device(id, name)
        dev.inet = 'inet'
        dev.inet6 = 'inet6'
        ns1 = Namespace('namespace')
        ns1.devices.append(dev)
        ns2 = Namespace('namespace')
        ns2.devices.append(dev)
        self.assertEqual(ns1, ns2)

    @mock.patch('pynet.models.execute_command')
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

    @mock.patch('pynet.models.execute_command')
    def test_device_discovery(self, execute_command):

        execute_command.side_effect = [
            self.ip_netns_list_output,
            self.ip_addr_list_output,
            self.ip_addr_list_output,
            self.ip_addr_list_output
        ]
        lo = Device('1', 'lo')
        lo.inet = '127.0.0.1/8'
        lo.inet6 = '::1/128'
        eth0 = Device('2', 'eth0')
        eth0.inet = '10.0.2.15/24'
        eth0.inet6 = 'fe80::a00:27ff:feea:67cf/64'
        docker0 = Device('3', 'docker0')
        docker0.inet = '172.17.42.1/16'
        docker0.inet6 = None

        namespaces = Namespace.discover(with_devices=True)

        self.assertEqual(len(namespaces), 3)
        for namespace in namespaces:
            self.assertEqual(len(namespace.devices), 3)
            self.assertTrue(lo in namespace.devices)
            self.assertTrue(eth0 in namespace.devices)
            self.assertTrue(docker0 in namespace.devices)


class TestDevice(unittest.TestCase):

    def setUp(self):
        self.ip_addr_list_output = open(IP_ADDR_RESULT).read()
        self.ip_netns_list_output = open(IP_NETNS_RESULT).read()


    def test_init_device(self):
        id = '1'
        name = 'eth0'
        dev = Device(id, name)
        self.assertEqual(dev.id, id)
        self.assertEqual(dev.name, name)
        self.assertFalse(dev.is_loopback())
        self.assertIsNone(dev.inet)
        self.assertIsNone(dev.inet6)

    def test_init_loopback(self):
        id = '1'
        name = 'lo'
        dev = Device(id, name)
        self.assertEqual(dev.id, id)
        self.assertEqual(dev.name, name)
        self.assertTrue(dev.is_loopback())

    def test_equality(self):
        dev1 = Device('id', 'name')
        dev2 = Device('id', 'name')
        self.assertEqual(dev1, dev2)

    @mock.patch('pynet.models.execute_command')
    def test_device_discovery(self, execute_command):

        execute_command.return_value = self.ip_addr_list_output
        lo = Device('1', 'lo')
        lo.inet = '127.0.0.1/8'
        lo.inet6 = '::1/128'
        eth0 = Device('2', 'eth0')
        eth0.inet = '10.0.2.15/24'
        eth0.inet6 = 'fe80::a00:27ff:feea:67cf/64'
        docker0 = Device('3', 'docker0')
        docker0.inet = '172.17.42.1/16'
        docker0.inet6 = None

        devices = Device.discover()

        self.assertEqual(len(devices), 3)
        self.assertTrue(lo in devices)
        self.assertTrue(eth0 in devices)
        self.assertTrue(docker0 in devices)

if __name__ == '__main__':
    unittest.main()
