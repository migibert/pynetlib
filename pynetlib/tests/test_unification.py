from __future__ import absolute_import
from pynetlib.unification import unify, discover_external_namespaces, unify_external_namespaces, unify_internal_namespaces
import mock
import unittest


class TestUnification(unittest.TestCase):

    @mock.patch('os.mkdir')
    @mock.patch('os.path.exists')
    @mock.patch('pynetlib.unification.unify_external_namespaces')
    @mock.patch('pynetlib.unification.unify_internal_namespaces')
    def test_unify_with_no_internal_namespaces(self, unify_external_namespaces, unify_internal_namespaces, exists, mkdir):
        exists.return_value = False
        unify()
        exists.assert_called_once_with('/var/run/netns')
        mkdir.assert_called_once_with('/var/run/netns')
        unify_external_namespaces.assert_called_once_with()
        unify_internal_namespaces.assert_called_once_with()

    @mock.patch('os.mkdir')
    @mock.patch('os.path.exists')
    @mock.patch('pynetlib.unification.unify_external_namespaces')
    @mock.patch('pynetlib.unification.unify_internal_namespaces')
    def test_unify_with_internal_namespaces(self, unify_external_namespaces, unify_internal_namespaces, exists, mkdir):
        exists.return_value = True
        unify()
        exists.assert_called_once_with('/var/run/netns')
        mkdir.assert_not_called()
        unify_external_namespaces.assert_called_once_with()
        unify_internal_namespaces.assert_called_once_with()

    @mock.patch('os.symlink')
    @mock.patch('os.path.islink')
    @mock.patch('pynetlib.unification.discover_external_namespaces')
    def test_unify_non_registered_external_namespaces(self, discover_external_namespaces, islink, symlink):
        discover_external_namespaces.return_value = [('pid', 'inode')]
        islink.return_value = False
        unify_external_namespaces()
        symlink.assert_called_once_with('/proc/pid/ns/net', '/var/run/netns/inode')

    @mock.patch('os.symlink')
    @mock.patch('os.path.islink')
    @mock.patch('pynetlib.unification.discover_external_namespaces')
    def test_unify_registered_external_namespaces(self, discover_external_namespaces, islink, symlink):
        discover_external_namespaces.return_value = [('pid', 'inode')]
        islink.return_value = True
        unify_external_namespaces()
        symlink.assert_not_called()

    @mock.patch('os.unlink')
    @mock.patch('os.listdir')
    @mock.patch('pynetlib.unification.discover_external_namespaces')
    def test_unify_non_existing_internal_namespaces(self, discover_external_namespaces, listdir, unlink):
        discover_external_namespaces.return_value = []
        listdir.return_value = ['net:[12345]']
        unify_internal_namespaces()
        unlink.assert_called_once_with('/var/run/netns/net:[12345]')

    @mock.patch('os.unlink')
    @mock.patch('os.listdir')
    @mock.patch('pynetlib.unification.discover_external_namespaces')
    def test_unify_existing_internal_namespaces(self, discover_external_namespaces, listdir, unlink):
        discover_external_namespaces.return_value = [('pid', 'net:[12345]')]
        listdir.return_value = ['net:[12345]']
        unify_internal_namespaces()
        unlink.assert_not_called()

    @mock.patch('os.unlink')
    @mock.patch('os.listdir')
    @mock.patch('pynetlib.unification.discover_external_namespaces')
    def test_unify_existing_internal_namespaces_created_from_ip_netns(self, discover_external_namespaces, listdir, unlink):
        discover_external_namespaces.return_value = []
        listdir.return_value = ['namespace']
        unify_internal_namespaces()
        unlink.assert_not_called()

    @mock.patch('fnmatch.filter')
    @mock.patch('os.readlink')
    def test_discover_external_namespaces(self, readlink, filter):
        readlink.side_effect = ['net:[4026531956]', 'net:[4026531956]', 'net:[12345]']
        filter.return_value = ['1', '2']
        ns = discover_external_namespaces()
        self.assertFalse(('1', 'net:[4026531956]') in ns)
        self.assertTrue(('2', 'net:[12345]') in ns)

    @mock.patch('fnmatch.filter')
    @mock.patch('os.readlink')
    def test_discover_external_namespaces_error(self, readlink, filter):
        readlink.side_effect = ['net:[4026531956]', OSError()]
        filter.return_value = ['1']
        ns = discover_external_namespaces()
        self.assertFalse(('1', 'net:[4026531956]') in ns)
        self.assertEqual([], ns)
