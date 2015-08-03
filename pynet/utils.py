import subprocess


def execute_command(command, namespace=None):
    if namespace is None or namespace.is_default():
        cmd = command
    else:
        cmd = 'ip netns exec %s %s' % (namespace.name, command)
    return subprocess.check_output(cmd, shell=True)
