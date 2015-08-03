from models import Namespace, Device
from utils import execute_command


class NetConf():
    def __init__(self, discover=True):
        self.namespaces = []
        if discover is True:
            self.discover()

    def discover(self):
        self.namespaces = self.discover_namespaces()
        for namespace in self.namespaces:
            namespace.devices = self.discover_devices(namespace)

    def discover_namespaces(self):
        default = Namespace(Namespace.DEFAULT_NAMESPACE_NAME)
        result = execute_command('ip netns list')
        return [default] + [Namespace(name) for name in result.split()]

    def discover_devices(self, namespace=None):
        output = execute_command('ip addr list', namespace)
        return self._parse_ip_result(output)

    def _parse_ip_result(self, command_out):
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
                    current_device.inet = self._find_value(words, 'inet')
                if current_device.inet6 is None:
                    current_device.inet6 = self._find_value(words, 'inet6')
        if current_device:
            devices.append(current_device)
        return devices

    def _find_value(self, values, key):
        if key in values:
            return values[values.index(key) + 1]
        return None


if __name__ == '__main__':
    nc = NetConf()
