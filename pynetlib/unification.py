import re
import os
import fnmatch

STANDARD_LOCATION = '/var/run/netns'


def get_inode(pid):
    return os.readlink('/proc/%s/ns/net' % pid)


def discover_external_namespaces():
    seen = []
    ns = []
    baseinode = get_inode('1')
    pidlist = fnmatch.filter(os.listdir('/proc/'), '[0123456789]*')
    for pid in pidlist:
        inode = get_inode(pid)
        if inode not in [None, '', baseinode, seen]:
            ns.append((pid, inode))
            seen.append(inode)
    return ns


def unify_external_namespaces():
    for pid, inode in discover_external_namespaces():
        src = '/proc/%s/ns/net' % pid
        dst = '%s/%s' % (STANDARD_LOCATION, inode)
        if not os.path.islink(dst):
            os.symlink(src, dst)


def unify_internal_namespaces():
    pattern = re.compile('^net\[(0-9)*]\]')
    internal_namespaces = [ns for ns in os.listdir(STANDARD_LOCATION) if pattern.match(ns)]
    external_namespaces = discover_external_namespaces()

    for internal_namespace in internal_namespaces:
        for pid, inode in external_namespaces:
            if inode == internal_namespace:
                break
        else:
            os.unlink('%s/%s' % (STANDARD_LOCATION, inode))


def unify():
    unify_internal_namespaces()
    unify_external_namespaces()


# unify_external_namespaces()
