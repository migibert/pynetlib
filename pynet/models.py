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
        self.inet = None
        self.inet6 = None

    def is_loopback(self):
        return self.name == 'lo'
