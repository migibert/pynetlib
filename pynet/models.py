from utils import execute_command, find_value


class Namespace():
    DEFAULT_NAMESPACE_NAME = ''

    def __init__(self, name):
        self.name = name
        self.devices = []

    def is_default(self):
        return self.name == Namespace.DEFAULT_NAMESPACE_NAME

    @staticmethod
    def discover(with_devices=False):
        default = Namespace(Namespace.DEFAULT_NAMESPACE_NAME)
        result = execute_command('ip netns list')
        namespaces = [default] + [Namespace(name) for name in result.split()]
        if with_devices:
            for namespace in namespaces:
                namespace.devices = Device.discover(namespace=namespace)
        return namespaces

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return '[' + self.name + ']'


class Device():
    def __init__(self, id, name, namespace=None):
        self.id = id
        self.name = name
        self.namespace = namespace
        self.inet = None
        self.inet6 = None

    def is_loopback(self):
        return self.name == 'lo'

    def add_address(self, address):
        execute_command('ip addr add %s dev %s' % (address, self.name), namespace=self.namespace)

    def remove_address(self, address):
        execute_command('ip addr del %s dev %s' % (address, self.name), namespace=self.namespace)

    @staticmethod
    def discover(namespace=None):
        output = execute_command('ip addr list', namespace)
        devices = []
        current_device = None
        for block in output.split('\n'):
            if block and block[0].isdigit():
                if current_device:
                    devices.append(current_device)
                prefixes = block.split(':')
                id = prefixes[0]
                name = prefixes[1].strip()
                current_device = Device(id, name, namespace=namespace)
            else:
                words = block.strip().split(' ')
                if current_device.inet is None:
                    current_device.inet = find_value(words, 'inet')
                if current_device.inet6 is None:
                    current_device.inet6 = find_value(words, 'inet6')
        if current_device:
            devices.append(current_device)
        return devices

    def __eq__(self, other):
        return \
            self.name == other.name and \
            self.id == other.id and \
            self.inet == other.inet and \
            self.inet6 == other.inet6

    def __repr__(self):
        return '[' + ','.join([self.id, self.name, str(self.inet), str(self.inet6)]) + ']'
