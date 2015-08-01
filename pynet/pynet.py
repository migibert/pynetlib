import subprocess

class Namespace():
    DEFAULT_NAMESPACE_NAME = ''

    def __init__(self, name):
        self.name = name
        self.devices = []

    def is_default(self):
        return self.name == Namespace.DEFAULT_NAMESPACE_NAME


class Device():
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def is_loopback(self):
        return self.name == 'lo'


class NetConf():
    def __init__(self):
        self.namespaces = []
        self.discover()

    def discover(self):
        self.namespaces = self.discover_namespaces()
        for namespace in self.namespaces:
            devices = self.discover_devices(namespace)
            namespace.devices = devices

    def discover_namespaces(self):
        default = Namespace(Namespace.DEFAULT_NAMESPACE_NAME)
        result = self._execute_command('ip netns list')
        return [default] + [Namespace(name) for name in result.split()]

    def discover_devices(self, namespace):
        output = self._execute_command('ip addr list', namespace)
        devices = []
        current_device = None
        for block in output.split('\n'):
            if block and block[0].isdigit():
                if current_device:
	            devices.append(current_device)
                firstSplit = block.split(':')
                id = firstSplit[0]
                name = firstSplit[1].strip()
                current_device = Device(id, name)
        if current_device:
            devices.append(current_device)
        return devices

    def _execute_command(self, command, namespace=None):
        if namespace is None or namespace.is_default():
            cmd = command
        else:
            cmd = 'ip netns exec %s %s' % (namespace.name, command)
        return subprocess.check_output(cmd, shell=True)

