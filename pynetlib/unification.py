import re
import os
import fnmatch

STANDARD_LOCATION = '/var/run/netns'
PROCESS_LOCATION = '/proc/%s/ns/net'


def discover_external_namespaces():
    seen = []
    ns = []
    baseinode = os.readlink(PROCESS_LOCATION % '1')
    pidlist = fnmatch.filter(os.listdir('/proc/'), '[0123456789]*')
    for pid in pidlist:
        try:
            inode = os.readlink(PROCESS_LOCATION % pid)
        except OSError:
            continue
        if inode not in [None, '', baseinode, seen]:
            ns.append((pid, inode))
            seen.append(inode)
    return ns


def unify_external_namespaces():
    for pid, inode in discover_external_namespaces():
        src = PROCESS_LOCATION % pid
        dst = '%s/%s' % (STANDARD_LOCATION, inode)
        if not os.path.islink(dst):
            os.symlink(src, dst)


def unify_internal_namespaces():
    pattern = re.compile('^net:\[([0-9])*\]$')
    internal_namespaces = [ns for ns in os.listdir(STANDARD_LOCATION) if pattern.match(ns)]
    external_namespaces = discover_external_namespaces()

    for internal_namespace in internal_namespaces:
        for pid, inode in external_namespaces:
            if inode == internal_namespace:
                break
        else:
            os.unlink('%s/%s' % (STANDARD_LOCATION, internal_namespace))


def unify():
    if not os.path.exists(STANDARD_LOCATION):
        os.mkdir(STANDARD_LOCATION)
    unify_internal_namespaces()
    unify_external_namespaces()
