from __builtin__ import staticmethod
import subprocess
from models import Namespace, Device


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
        return self._parse_ip_result(output)

    @staticmethod
    def _execute_command(command, namespace=None):
        if namespace is None or namespace.is_default():
            cmd = command
        else:
            cmd = 'ip netns exec %s %s' % (namespace.name, command)
        return subprocess.check_output(cmd, shell=True)

    @staticmethod
    def _parse_ip_result(command_out):
        devices = []
        current_device = None
        for block in command_out.split('\n'):
            if block and block[0].isdigit():
                if current_device:
                    devices.append(current_device)
                first_split = block.split(':')
                id = first_split[0]
                name = first_split[1].strip()
                current_device = Device(id, name)
            else:
                words = block.strip().split(' ')
                if current_device.inet is None:
                    current_device.inet = NetConf._find_value(words, 'inet')
                if current_device.inet6 is None:
                    current_device.inet6 = NetConf._find_value(words, 'inet6')
        if current_device:
            devices.append(current_device)
        return devices

    @staticmethod
    def _find_value(values, key):
        if key in values:
            return values[values.index(key) + 1]
        return None
