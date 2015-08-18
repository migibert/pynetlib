from utils import execute_command, find_value
from exceptions import ObjectAlreadyExistsException, ObjectNotFoundException, ForbiddenException


class Namespace():
    DEFAULT_NAMESPACE_NAME = ''

    def __init__(self, name):
        self.name = name
        self.devices = []

    def is_default(self):
        return self.name == Namespace.DEFAULT_NAMESPACE_NAME

    def exists(self):
        return self in Namespace.discover()

    def create(self):
        if self.is_default() or self.exists():
            raise ObjectAlreadyExistsException(self)
        execute_command('ip netns add %s' % self.name)

    def delete(self):
        if self.is_default():
            raise ForbiddenException('Default namespace deletion is not possible')
        if not self.exists():
            raise ObjectNotFoundException(self)
        execute_command('ip netns del %s' % self.name)

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
    def __init__(self, id, name, flags=[], namespace=None):
        self.id = id
        self.name = name
        self.flags = flags
        self.namespace = namespace
        self.state = None
        self.inet = []
        self.inet6 = []

    def is_loopback(self):
        return 'LOOPBACK' in self.flags

    def is_multicast(self):
        return 'MULTICAST' in self.flags

    def is_broadcast(self):
        return 'BROADCAST' in self.flags

    def is_up(self):
        return 'UP' in self.flags

    def is_down(self):
        return 'LOWER_UP' not in self.flags and not self.is_up()

    def add_address(self, address):
        if self.contains_address(address):
            raise ObjectAlreadyExistsException(address)
        execute_command('ip addr add %s dev %s' % (address, self.name), namespace=self.namespace)
        self.refresh()

    def remove_address(self, address):
        if not self.contains_address(address):
            raise ObjectNotFoundException(address)
        execute_command('ip addr del %s dev %s' % (address, self.name), namespace=self.namespace)
        self.refresh()

    def contains_address(self, address):
        return address in self.inet + self.inet6

    def enable(self):
        if self.is_down():
            execute_command('ip link set %s up' % self.name, namespace=self.namespace)
            self.refresh()

    def disable(self):
        if not self.is_down():
            execute_command('ip link set %s down' % self.name, namespace=self.namespace)
            self.refresh()

    def refresh(self):
        output = execute_command('ip addr show %s' % self.name, namespace=self.namespace)
        devices = Device.parse_output(output, namespace=self.namespace)
        if len(devices) != 1:
            raise Exception('Only one device can be named %s inside the same namespace' % self.name)
        dev = devices[0]
        self.id = dev.id
        self.name = dev.name
        self.flags = dev.flags
        self.namespace = dev.namespace
        self.state = dev.state
        self.inet = dev.inet
        self.inet6 = dev.inet6

    @staticmethod
    def discover(namespace=None):
        output = execute_command('ip addr list', namespace=namespace)
        return Device.parse_output(output, namespace=namespace)

    @staticmethod
    def parse_output(output, namespace=None):
        devices = []
        current_device = None
        for block in output.split('\n'):
            if block and block[0].isdigit():
                if current_device:
                    devices.append(current_device)
                prefixes = block.split(':')
                id = prefixes[0]
                name = prefixes[1].strip()
                flags = block[block.index('<') + 1:block.index('>')].split(',')
                current_device = Device(id, name, flags=flags, namespace=namespace)
            else:
                words = block.strip().split(' ')
                state = find_value(words, 'state')
                if state is not None:
                    current_device.state = state
                inet = find_value(words, 'inet')
                if inet is not None:
                    current_device.inet.append(inet)
                inet6 = find_value(words, 'inet6')
                if inet6 is not None:
                    current_device.inet6.append(inet6)
        if current_device:
            devices.append(current_device)
        return devices

    def __eq__(self, other):
        return self.name == other.name and self.id == other.id

    def __repr__(self):
        return '[' + ','.join([self.id, self.name, str(self.inet), str(self.inet6)]) + ']'
