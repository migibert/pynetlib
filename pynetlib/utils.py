import subprocess
from pynetlib.exceptions import ValueNotFoundException


def execute_command(command, namespace=None):
    ns = namespace
    if hasattr(namespace, 'name'):
        ns = namespace.name
    if ns is None or ns == '':
        cmd = command
    else:
        cmd = 'ip netns exec %s %s' % (ns, command)
    return subprocess.check_output(cmd, shell=True)


def find_value(values, key):
    if key in values:
        if len(values) > values.index(key) + 1:
            return values[values.index(key) + 1]
        raise ValueNotFoundException('Value not found for key %s' % key)
    return None
