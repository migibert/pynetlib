import subprocess


def execute_command(command, namespace=None):
    if namespace is None or namespace.is_default():
        cmd = command
    else:
        cmd = 'ip netns exec %s %s' % (namespace.name, command)
    return subprocess.check_output(cmd, shell=True)


def find_value(values, key):
    if key in values:
        return values[values.index(key) + 1]
    return None
