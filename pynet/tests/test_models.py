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


class TestDevice(unittest.TestCase):
    def test_init(self):
        id = '1'
        name = 'eth0'
        dev = Device(id, name)
        self.assertEqual(dev.id, id)
        self.assertEqual(dev.name, name)
        self.assertFalse(dev.is_loopback())

    def test_init_default(self):
        id = '1'
        name = 'lo'
        dev = Device(id, name)
        self.assertEqual(dev.id, id)
        self.assertEqual(dev.name, name)
        self.assertTrue(dev.is_loopback())


if __name__ == '__main__':
    unittest.main()
