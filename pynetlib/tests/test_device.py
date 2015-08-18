import os
import mock
import unittest
from pynetlib.models import Namespace, Device
from pynetlib.exceptions import ObjectNotFoundException, ObjectAlreadyExistsException

IP_ADDR_LIST_RESULT = os.path.join(os.path.dirname(__file__) + '/fixtures', 'ip_addr_list')
IP_ADDR_SHOW_RESULT = os.path.join(os.path.dirname(__file__) + '/fixtures', 'ip_addr_show')


class TestDevice(unittest.TestCase):

    def setUp(self):
        self.ip_addr_list_output = open(IP_ADDR_LIST_RESULT).read()
        self.ip_addr_show_output = open(IP_ADDR_SHOW_RESULT).read()

    def test_init_device(self):
        id = '1'
        name = 'eth0'
        dev = Device(id, name)
        self.assertEqual(dev.id, id)
        self.assertEqual(dev.name, name)
        self.assertFalse(dev.is_loopback())
        self.assertEqual(dev.inet, [])
        self.assertEqual(dev.inet6, [])

    def test_init_loopback(self):
        id = '1'
        name = 'lo'
        flags = ['LOOPBACK']
        dev = Device(id, name, flags=flags)
        self.assertEqual(dev.id, id)
        self.assertEqual(dev.name, name)
        self.assertTrue(dev.is_loopback())

    def test_broadcast_when_flag_is_present(self):
        dev = Device('1', 'eth0', flags=['BROADCAST'])
        self.assertTrue(dev.is_broadcast())

    def test_broadcast_when_flag_is_not_present(self):
        dev = Device('1', 'eth0', flags=[])
        self.assertFalse(dev.is_broadcast())

    def test_multicast_when_flag_is_present(self):
        dev = Device('1', 'eth0', flags=['MULTICAST'])
        self.assertTrue(dev.is_multicast())

    def test_multicast_when_flag_is_not_present(self):
        dev = Device('1', 'eth0', flags=[])
        self.assertFalse(dev.is_multicast())

    def test_up_when_flag_is_present(self):
        dev = Device('1', 'eth0', flags=['UP'])
        self.assertTrue(dev.is_up())

    def test_up_when_flag_is_not_present(self):
        dev = Device('1', 'eth0', flags=[])
        self.assertFalse(dev.is_up())

    def test_down_when_flag_is_present(self):
        dev = Device('1', 'eth0', flags=['DOWN'])
        self.assertTrue(dev.is_down())

    def test_up_when_flag_is_not_present(self):
        dev = Device('1', 'eth0', flags=[])
        self.assertTrue(dev.is_down())

    def test_up_when_up_flag_is_present(self):
        dev = Device('1', 'eth0', flags=['UP'])
        self.assertFalse(dev.is_down())

    def test_up_when_lower_up_flag_is_present(self):
        dev = Device('1', 'eth0', flags=['LOWER_UP'])
        self.assertFalse(dev.is_down())

    def test_equality(self):
        dev1 = Device('id', 'name')
        dev2 = Device('id', 'name')
        self.assertEqual(dev1, dev2)

    @mock.patch('pynetlib.models.execute_command')
    def test_device_discovery(self, execute_command):
        execute_command.return_value = self.ip_addr_list_output
        lo = Device('1', 'lo')
        lo.flags = ['LOOPBACK', 'UP', 'LOWER_UP']
        lo.inet = ['127.0.0.1/8']
        lo.inet6 = ['::1/128']
        eth0 = Device('2', 'eth0')
        eth0.flags = ['BROADCAST', 'MULTICAST', 'UP', 'LOWER_UP']
        eth0.inet = ['10.0.2.15/24', '10.0.2.16/24']
        eth0.inet6 = ['fe80::a00:27ff:feea:67cf/64']
        docker0 = Device('3', 'docker0')
        docker0.flags = ['NO-CARRIER', 'BROADCAST', 'MULTICAST', 'UP']
        docker0.inet = ['172.17.42.1/16']
        docker0.inet6 = []

        devices = Device.discover()

        self.assertEqual(len(devices), 3)
        self.assertTrue(lo in devices)
        self.assertTrue(eth0 in devices)
        self.assertTrue(docker0 in devices)

        for device in devices:
            if device is lo:
                self.assertEqual(device.flags, lo.flags)
                self.assertEqual(device.inet, lo.inet)
                self.assertEqual(device.inet6, lo.inet6)
            if device is eth0:
                self.assertEqual(device.flags, eth0.flags)
                self.assertEqual(device.inet, eth0.inet)
                self.assertEqual(device.inet6, eth0.inet6)
            if device is docker0:
                self.assertEqual(device.flags, docker0.flags)
                self.assertEqual(device.inet, docker0.inet)
                self.assertEqual(device.inet6, docker0.inet6)

    @mock.patch('pynetlib.models.execute_command')
    def test_device_namespace_discovery(self, execute_command):
        namespace = Namespace('namespace')
        execute_command.return_value = self.ip_addr_list_output
        lo = Device('1', 'lo')
        lo.inet = ['127.0.0.1/8']
        lo.inet6 = ['::1/128']
        eth0 = Device('2', 'eth0')
        eth0.inet = ['10.0.2.15/24', '10.0.2.16/24']
        eth0.inet6 = ['fe80::a00:27ff:feea:67cf/64']
        docker0 = Device('3', 'docker0')
        docker0.inet = ['172.17.42.1/16']
        docker0.inet6 = []

        devices = Device.discover(namespace=namespace)

        self.assertEqual(len(devices), 3)
        self.assertTrue(lo in devices)
        self.assertTrue(eth0 in devices)
        self.assertTrue(docker0 in devices)
        for device in devices:
            self.assertEqual(device.namespace, namespace)

    @mock.patch('pynetlib.models.execute_command')
    def test_add_address_to_device_on_default_namespace(self, execute_command):
        dev = Device('1', 'eth0')
        dev.refresh = mock.Mock()
        dev.add_address('192.168.10.10')
        execute_command.assert_called_once_with('ip addr add 192.168.10.10 dev eth0', namespace=None)
        dev.refresh.assert_called_once_with()

    @mock.patch('pynetlib.models.execute_command')
    def test_add_existing_address_to_device(self, execute_command):
        dev = Device('1', 'eth0')
        dev.refresh = mock.Mock()
        dev.inet = ['192.168.10.10/32']
        with self.assertRaises(ObjectAlreadyExistsException):
            dev.add_address('192.168.10.10/32')
        execute_command.assert_not_called()
        dev.refresh.assert_not_called

    @mock.patch('pynetlib.models.execute_command')
    def test_add_address_to_device_on_specific_namespace(self, execute_command):
        ns = Namespace('ns')
        dev = Device('1', 'eth0', namespace=ns)
        dev.refresh = mock.Mock()
        dev.add_address('192.168.10.10')
        execute_command.assert_called_once_with('ip addr add 192.168.10.10 dev eth0', namespace=ns)
        dev.refresh.assert_called_once_with()

    @mock.patch('pynetlib.models.execute_command')
    def test_remove_address_from_device_on_default_namespace(self, execute_command):
        dev = Device('1', 'eth0')
        dev.refresh = mock.Mock()
        dev.inet = ['192.168.10.10/32']
        dev.remove_address('192.168.10.10/32')
        execute_command.assert_called_once_with('ip addr del 192.168.10.10/32 dev eth0', namespace=None)
        dev.refresh.assert_called_once_with()

    @mock.patch('pynetlib.models.execute_command')
    def test_remove_address_from_device_on_specific_namespace(self, execute_command):
        ns = Namespace('ns')
        dev = Device('1', 'eth0', namespace=ns)
        dev.refresh = mock.Mock()
        dev.inet = ['192.168.10.10/32']
        dev.remove_address('192.168.10.10/32')
        execute_command.assert_called_once_with('ip addr del 192.168.10.10/32 dev eth0', namespace=ns)
        dev.refresh.assert_called_once_with()

    @mock.patch('pynetlib.models.execute_command')
    def test_remove_non_existing_address_from_device(self, execute_command):
        dev = Device('1', 'eth0')
        dev.refresh = mock.Mock()
        with self.assertRaises(ObjectNotFoundException):
            dev.remove_address('192.168.10.10/32')
        execute_command.assert_not_called()
        dev.refresh.assert_not_called()

    def test_exists_address_from_device(self):
        address = '192.168.42.42'
        dev = Device('1', 'eth0')
        dev.inet = ['10.0.2.15/24', address]
        dev.inet6 = []
        self.assertTrue(dev.contains_address(address))

    def test_exists_non_existing_address_from_device(self):
        dev = Device('1', 'eth0')
        dev.inet = []
        dev.inet6 = []
        self.assertFalse(dev.contains_address('192.168.42.42'))

    def test_exists_inet6_address_from_device(self):
        address = 'fe80::a00:27ff:feea:67cf/64'
        dev = Device('1', 'eth0')
        dev.inet = []
        dev.inet6 = [address]
        self.assertTrue(dev.contains_address(address))

    def test_exists_non_existing_inet6_address_from_device(self):
        dev = Device('1', 'eth0')
        dev.inet = []
        dev.inet6 = []
        self.assertFalse(dev.contains_address('fe80::a00:27ff:feea:67cf/64'))

    @mock.patch('pynetlib.models.execute_command')
    def test_enable_up_device(self, execute_command):
        dev = Device('1', 'eth0')
        dev.refresh = mock.Mock()
        dev.flags = ['UP']
        dev.enable()
        execute_command.assert_not_called()
        dev.refresh.assert_not_called()

    @mock.patch('pynetlib.models.execute_command')
    def test_enable_down_device(self, execute_command):
        dev = Device('1', 'eth0')
        dev.refresh = mock.Mock()
        dev.flags = []
        dev.enable()
        execute_command.assert_called_once_with("ip link set eth0 up", namespace=None)
        dev.refresh.assert_called_once_with()

    @mock.patch('pynetlib.models.execute_command')
    def test_disable_up_device(self, execute_command):
        dev = Device('1', 'eth0')
        dev.refresh = mock.Mock()
        dev.flags = ['UP']
        dev.disable()
        execute_command.assert_called_once_with("ip link set eth0 down", namespace=None)
        dev.refresh.assert_called_once_with()

    @mock.patch('pynetlib.models.execute_command')
    def test_enable_down_device(self, execute_command):
        dev = Device('1', 'eth0')
        dev.refresh = mock.Mock()
        dev.flags = []
        dev.disable()
        execute_command.assert_not_called()
        dev.refresh.assert_not_called()

    @mock.patch('pynetlib.models.execute_command')
    def test_refresh_device(self, execute_command):
        execute_command.return_value = self.ip_addr_show_output
        device = Device('1', 'eth0')
        device.flags = []
        device.refresh()
        execute_command.assert_called_once_with("ip addr show eth0", namespace=None)
        self.assertEqual(device.id, '2')
        self.assertEqual(device.name, "eth0")
        self.assertEqual(device.flags, ['BROADCAST', 'MULTICAST', 'UP', 'LOWER_UP'])
        self.assertEqual(device.inet, ['10.0.2.15/24'])
        self.assertEqual(device.inet6, ['fe80::a00:27ff:feea:67cf/64'])
        self.assertIsNone(device.namespace)


if __name__ == '__main__':
    unittest.main()
