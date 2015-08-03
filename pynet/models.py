class Namespace():
    DEFAULT_NAMESPACE_NAME = ''

    def __init__(self, name):
        self.name = name
        self.devices = []

    def is_default(self):
        return self.name == Namespace.DEFAULT_NAMESPACE_NAME

    def __eq__(self, other):
        return self.name == other.name and self.devices == other.devices

    def __repr__(self):
        return '[' + self.name + ']'


class Device():
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.inet = None
        self.inet6 = None

    def is_loopback(self):
        return self.name == 'lo'

    def __eq__(self, other):
        return \
            self.name == other.name and \
            self.id == other.id and \
            self.inet == other.inet and \
            self.inet6 == other.inet6

    def __repr__(self):
        return '[' + ','.join([self.id, self.name, str(self.inet), str(self.inet6)]) + ']'
