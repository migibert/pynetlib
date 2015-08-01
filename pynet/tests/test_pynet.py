import unittest
from pynet.models import Namespace, Device

class TestNamespace(unittest.TestCase):
    def test_init(self):
        name = 'mynamespace'
        ns = Namespace(name)
        self.assertEqual(ns.name, name)
        self.assertEqual(len(ns.devices), 0)

if __name__ == '__main__':
    unittest.main()
