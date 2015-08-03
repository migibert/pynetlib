import unittest
from pynet.models import Namespace, Device


class TestNamespace(unittest.TestCase):
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


class TestDevice(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main()
