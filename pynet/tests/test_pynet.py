import unittest
import mock
import os
from pynet.pynet import NetConf
from pynet.models import Namespace, Device

IP_ADDR_RESULT = os.path.join(os.path.dirname(__file__) + '/fixtures', 'ip_addr_list')
IP_NETNS_RESULT = os.path.join(os.path.dirname(__file__) + '/fixtures', 'ip_netns_list')


class TestPynet(unittest.TestCase):

    def setUp(self):
        self.ip_addr_list_output = open(IP_ADDR_RESULT).read()
        self.ip_netns_list_output = open(IP_NETNS_RESULT).read()

    @mock.patch('pynet.pynet.execute_command')
    def test_namespace_discovery(self, execute_command):

        execute_command.return_value = self.ip_netns_list_output
        default_namespace = Namespace('')
        first_namespace = Namespace('first_namespace')
        second_namespace = Namespace('second_namespace')

        netconf = NetConf(discover=False)
        namespaces = netconf.discover_namespaces()

        self.assertEqual(len(namespaces), 3)
        self.assertTrue(default_namespace in namespaces)
        self.assertTrue(first_namespace in namespaces)
        self.assertTrue(second_namespace in namespaces)

    @mock.patch('pynet.pynet.execute_command')
    def test_namespace_discovery(self, execute_command):

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

        netconf = NetConf(discover=False)
        devices = netconf.discover_devices()

        self.assertEqual(len(devices), 3)
        self.assertTrue(lo in devices)
        self.assertTrue(eth0 in devices)
        self.assertTrue(docker0 in devices)

    @mock.patch('pynet.pynet.execute_command')
    def test_netconf_discovery(self, execute_command):

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

        netconf = NetConf(discover=True)

        self.assertEqual(len(netconf.namespaces), 3)
        for namespace in netconf.namespaces:
            self.assertEqual(len(namespace.devices), 3)
            self.assertTrue(lo in namespace.devices)
            self.assertTrue(eth0 in namespace.devices)
            self.assertTrue(docker0 in namespace.devices)


if __name__ == '__main__':
    unittest.main()
