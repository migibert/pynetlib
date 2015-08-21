import os
import fnmatch


def get_inode(pid):
    return os.readlink('/proc/%s/ns/net' % pid)


def deduplicate_external_namespaces(external_namespaces):
    result = []
    seen_names = []
    for pid, inode in external_namespaces:
        if inode not in seen_names:
            seen_names.append(inode)
            res = {'pids': [pid], 'inode': inode}
            result.append(res)
    return result


def discover_external_namespaces():
    ns = []
    baseinode = get_inode('1')
    pidlist = fnmatch.filter(os.listdir('/proc/'), '[0123456789]*')
    for pid in pidlist:
        inode = get_inode(pid)
        if inode not in [None, '', baseinode]:
            ns.append((pid, inode))
    return deduplicate_external_namespaces(ns)


def unify_external_namespaces():
    for namespace in discover_external_namespaces():
        dst = '/var/run/netns/%s' % namespace['inode']
        if not os.path.islink(dst):
            os.symlink('/proc/%s/ns/net' % namespace['pid'], dst)


# unify_external_namespaces()
