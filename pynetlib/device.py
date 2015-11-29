from __future__ import absolute_import
from .utils import execute_command, get_devices_info
from .exceptions import ObjectAlreadyExistsException, ObjectNotFoundException
from . import NetworkBase


class Device(NetworkBase):
    def __init__(self, id, name, flags=[], namespace=None):
        self.id = id
        self.name = name
        self.flags = flags
        self.namespace = namespace
        self.state = None
        self.inet = []
        self.inet6 = []
        self.mtu = None
        self.qlen = None
        self.qdisc = None

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
        devices = Device.discover(namespace=self.namespace)
        if self not in devices:
            raise ObjectNotFoundException(self)
        found = devices[devices.index(self)]
        self.flags = found.flags
        self.inet = found.inet
        self.inet6 = found.inet6
        self.mtu = found.mtu
        self.qlen = found.qlen
        self.qdisc = found.qdisc

    @staticmethod
    def discover(namespace=None):
        devices = []
        output = execute_command('ip addr list', namespace=namespace)
        for id, name, flags, state, inet, inet6, mtu, qlen, qdisc in get_devices_info(output):
            device = Device(id, name, flags=flags, namespace=namespace)
            device.state = state
            device.inet = inet
            device.inet6 = inet6
            device.mtu = mtu
            device.qlen = qlen
            device.qdisc = qdisc
            devices.append(device)
        return devices

    def __eq__(self, other):
        return self.name == other.name and self.id == other.id
