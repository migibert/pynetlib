from __future__ import absolute_import
import mock
import unittest
from . import read_file
from nose_parameterized import parameterized
from pynetlib.device import Device
from pynetlib.namespace import Namespace
from pynetlib.exceptions import ObjectNotFoundException, ObjectAlreadyExistsException


class TestDevice(unittest.TestCase):

    def setUp(self):
        self.ip_addr_list_output = read_file('ip_addr_list')

    def test_init_device(self):
        id = '1'
        name = 'eth0'
        dev = Device(id, name)
        self.assertEqual(dev.id, id)
        self.assertEqual(dev.name, name)
        self.assertFalse(dev.is_loopback())
        self.assertEqual(dev.inet, [])
        self.assertEqual(dev.inet6, [])
        self.assertIsNone(dev.state)
        self.assertIsNone(dev.mtu)
        self.assertIsNone(dev.qlen)
        self.assertIsNone(dev.qdisc)

    def test_init_loopback(self):
        id = '1'
        name = 'lo'
        flags = ['LOOPBACK']
        dev = Device(id, name, flags=flags)
        self.assertEqual(dev.id, id)
        self.assertEqual(dev.name, name)
        self.assertTrue(dev.is_loopback())

    @parameterized.expand([
        (['UP'], (True, False, False, False)),
        (['LOWER_UP'], (False, False, False, False)),
        (['DOWN'], (False, True, False, False)),
        ([], (False, True, False, False)),
        (['BROADCAST'], (False, True, True, False)),
        (['MULTICAST'], (False, True, False, True)),
        (['UP', 'BROADCAST', 'MULTICAST'], (True, False, True, True))
    ])
    def test_flags(self, flags, statuses):
        is_up, is_down, is_broadcast, is_multicast = statuses
        dev = Device('1', 'eth0', flags=flags)
        self.assertEqual(dev.is_up(), is_up)
        self.assertEqual(dev.is_down(), is_down)
        self.assertEqual(dev.is_broadcast(), is_broadcast)
        self.assertEqual(dev.is_multicast(), is_multicast)

    def test_equality(self):
        dev1 = Device('id', 'name')
        dev2 = Device('id', 'name')
        self.assertEqual(dev1, dev2)

    @parameterized.expand([
        ('1', 'lo', ['LOOPBACK', 'UP', 'LOWER_UP'], ['127.0.0.1/8'], ['::1/128'], 'UNKNOWN', '65536', None, 'noqueue'),
        ('2', 'eth0', ['BROADCAST', 'MULTICAST', 'UP', 'LOWER_UP'], ['10.0.2.15/24', '10.0.2.16/24'], ['fe80::a00:27ff:feea:67cf/64'], 'UP', '1500', '1000', 'pfifo_fast'),
        ('3', 'docker0', ['NO-CARRIER', 'BROADCAST', 'MULTICAST', 'UP'], ['172.17.42.1/16'], [], 'DOWN', '1500', None, 'noqueue')
    ])
    @mock.patch('pynetlib.device.execute_command')
    def test_device_discovery(self, id, name, flags, inet, inet6, state, mtu, qlen, qdisc, execute_command):
        execute_command.return_value = self.ip_addr_list_output
        device = Device(id, name, flags=flags)

        devices = Device.discover()

        self.assertEqual(len(devices), 3)
        self.assertTrue(device in devices)
        found_device = devices[devices.index(device)]
        self.assertEqual(found_device.flags, device.flags)
        self.assertEqual(found_device.inet, inet)
        self.assertEqual(found_device.inet6, inet6)
        self.assertEqual(found_device.state, state)
        self.assertEqual(found_device.mtu, mtu)
        self.assertEqual(found_device.qlen, qlen)
        self.assertEqual(found_device.qdisc, qdisc)

    @parameterized.expand([
        ('1', 'lo', ['127.0.0.1/8'], ['::1/128']),
        ('2', 'eth0', ['10.0.2.15/24', '10.0.2.16/24'], ['fe80::a00:27ff:feea:67cf/64']),
        ('3', 'docker0', ['172.17.42.1/16'], [])
    ])
    @mock.patch('pynetlib.device.execute_command')
    def test_device_namespace_discovery(self, id, name, inet, inet6, execute_command):
        namespace = Namespace('namespace')
        execute_command.return_value = self.ip_addr_list_output
        device = Device(id, name)
        device.inet = inet
        device.inet6 = inet6
        device.namespace = namespace

        devices = Device.discover(namespace=namespace)

        self.assertEqual(len(devices), 3)
        self.assertTrue(device in devices)
        self.assertEqual(device.namespace, namespace)

    @mock.patch('pynetlib.device.execute_command')
    def test_add_address_to_device_on_default_namespace(self, execute_command):
        dev = Device('1', 'eth0')
        dev.refresh = mock.Mock()
        dev.add_address('192.168.10.10')
        execute_command.assert_called_once_with('ip addr add 192.168.10.10 dev eth0', namespace=None)
        dev.refresh.assert_called_once_with()

    @mock.patch('pynetlib.device.execute_command')
    def test_add_existing_address_to_device(self, execute_command):
        dev = Device('1', 'eth0')
        dev.refresh = mock.Mock()
        dev.inet = ['192.168.10.10/32']
        with self.assertRaises(ObjectAlreadyExistsException):
            dev.add_address('192.168.10.10/32')
        execute_command.assert_not_called()
        dev.refresh.assert_not_called

    @mock.patch('pynetlib.device.execute_command')
    def test_add_address_to_device_on_specific_namespace(self, execute_command):
        ns = Namespace('ns')
        dev = Device('1', 'eth0', namespace=ns)
        dev.refresh = mock.Mock()
        dev.add_address('192.168.10.10')
        execute_command.assert_called_once_with('ip addr add 192.168.10.10 dev eth0', namespace=ns)
        dev.refresh.assert_called_once_with()

    @mock.patch('pynetlib.device.execute_command')
    def test_remove_address_from_device_on_default_namespace(self, execute_command):
        dev = Device('1', 'eth0')
        dev.refresh = mock.Mock()
        dev.inet = ['192.168.10.10/32']
        dev.remove_address('192.168.10.10/32')
        execute_command.assert_called_once_with('ip addr del 192.168.10.10/32 dev eth0', namespace=None)
        dev.refresh.assert_called_once_with()

    @mock.patch('pynetlib.device.execute_command')
    def test_remove_address_from_device_on_specific_namespace(self, execute_command):
        ns = Namespace('ns')
        dev = Device('1', 'eth0', namespace=ns)
        dev.refresh = mock.Mock()
        dev.inet = ['192.168.10.10/32']
        dev.remove_address('192.168.10.10/32')
        execute_command.assert_called_once_with('ip addr del 192.168.10.10/32 dev eth0', namespace=ns)
        dev.refresh.assert_called_once_with()

    @mock.patch('pynetlib.device.execute_command')
    def test_remove_non_existing_address_from_device(self, execute_command):
        dev = Device('1', 'eth0')
        dev.refresh = mock.Mock()
        with self.assertRaises(ObjectNotFoundException):
            dev.remove_address('192.168.10.10/32')
        execute_command.assert_not_called()
        dev.refresh.assert_not_called()

    @parameterized.expand([('192.168.42.42', ['192.168.42.42'], True), ('192.168.42.42', [], False)])
    def test_exists_address_from_device(self, address, addresses, exists):
        dev = Device('1', 'eth0')
        dev.inet = addresses
        dev.inet6 = []
        self.assertEqual(dev.contains_address(address), exists)

    @parameterized.expand([
        ('fe80::a00:27ff:feea:67cf/64', ['fe80::a00:27ff:feea:67cf/64'], True),
        ('fe80::a00:27ff:feea:67cf/64', [], False),
    ])
    def test_exists_inet6_address_from_device(self, address, addresses, exists):
        dev = Device('1', 'eth0')
        dev.inet = []
        dev.inet6 = addresses
        self.assertEqual(dev.contains_address(address), exists)

    @mock.patch('pynetlib.device.execute_command')
    def test_enable_up_device(self, execute_command):
        dev = Device('1', 'eth0', flags=['UP'])
        dev.refresh = mock.Mock()
        dev.enable()
        execute_command.assert_not_called()
        dev.refresh.assert_not_called()

    @mock.patch('pynetlib.device.execute_command')
    def test_enable_down_device(self, execute_command):
        dev = Device('1', 'eth0', flags=[])
        dev.refresh = mock.Mock()
        dev.enable()
        execute_command.assert_called_once_with("ip link set eth0 up", namespace=None)
        dev.refresh.assert_called_once_with()

    @mock.patch('pynetlib.device.execute_command')
    def test_disable_up_device(self, execute_command):
        dev = Device('1', 'eth0', flags=['UP'])
        dev.refresh = mock.Mock()
        dev.disable()
        execute_command.assert_called_once_with("ip link set eth0 down", namespace=None)
        dev.refresh.assert_called_once_with()

    @mock.patch('pynetlib.device.execute_command')
    def test_disable_down_device(self, execute_command):
        dev = Device('1', 'eth0', flags=[])
        dev.refresh = mock.Mock()
        dev.disable()
        execute_command.assert_not_called()
        dev.refresh.assert_not_called()

    @mock.patch('pynetlib.device.execute_command')
    def test_refresh_device(self, execute_command):
        execute_command.return_value = self.ip_addr_list_output
        device = Device('2', 'eth0', flags=[])
        device.refresh()
        execute_command.assert_called_once_with("ip addr list", namespace=None)
        self.assertEqual(device.id, '2')
        self.assertEqual(device.name, 'eth0')
        self.assertEqual(device.flags, ['BROADCAST', 'MULTICAST', 'UP', 'LOWER_UP'])
        self.assertEqual(device.inet, ['10.0.2.15/24', '10.0.2.16/24'])
        self.assertEqual(device.inet6, ['fe80::a00:27ff:feea:67cf/64'])
        self.assertEqual(device.mtu, '1500')
        self.assertEqual(device.qlen, '1000')
        self.assertEqual(device.qdisc, 'pfifo_fast')
        self.assertIsNone(device.namespace)

    @mock.patch('pynetlib.device.execute_command')
    def test_refresh_non_existing_device(self, execute_command):
        execute_command.return_value = self.ip_addr_list_output
        device = Device('id', 'device', flags=[])
        with self.assertRaises(ObjectNotFoundException):
            device.refresh()
            execute_command.assert_called_once_with("ip addr list", namespace=None)
