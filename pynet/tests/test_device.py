import os
import mock
import unittest
from pynet.models import Namespace, Device

IP_ADDR_RESULT = os.path.join(os.path.dirname(__file__) + '/fixtures', 'ip_addr_list')


class TestDevice(unittest.TestCase):

    def setUp(self):
        self.ip_addr_list_output = open(IP_ADDR_RESULT).read()

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

    @mock.patch('pynet.models.execute_command')
    def test_device_namespace_discovery(self, execute_command):
        namespace = Namespace('namespace')
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

        devices = Device.discover(namespace=namespace)

        self.assertEqual(len(devices), 3)
        self.assertTrue(lo in devices)
        self.assertTrue(eth0 in devices)
        self.assertTrue(docker0 in devices)
        for device in devices:
            self.assertEqual(device.namespace, namespace)

    @mock.patch('pynet.models.execute_command')
    def test_add_address_to_device_on_default_namespace(self, execute_command):
        dev = Device('1', 'eth0')
        dev.add_address('192.168.10.10')
        execute_command.assert_called_once_with('ip addr add 192.168.10.10 dev eth0', namespace=None)

    @mock.patch('pynet.models.execute_command')
    def test_add_address_to_device_on_specific_namespace(self, execute_command):
        ns = Namespace('ns')
        dev = Device('1', 'eth0', namespace=ns)
        dev.add_address('192.168.10.10')
        execute_command.assert_called_once_with('ip addr add 192.168.10.10 dev eth0', namespace=ns)

    @mock.patch('pynet.models.execute_command')
    def test_remove_address_from_device_on_default_namespace(self, execute_command):
        dev = Device('1', 'eth0')
        dev.remove_address('192.168.10.10')
        execute_command.assert_called_once_with('ip addr del 192.168.10.10 dev eth0', namespace=None)

    @mock.patch('pynet.models.execute_command')
    def test_remove_address_from_device_on_specific_namespace(self, execute_command):
        ns = Namespace('ns')
        dev = Device('1', 'eth0', namespace=ns)
        dev.remove_address('192.168.10.10')
        execute_command.assert_called_once_with('ip addr del 192.168.10.10 dev eth0', namespace=ns)


if __name__ == '__main__':
    unittest.main()
