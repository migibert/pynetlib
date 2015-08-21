from utils import execute_command
from exceptions import ObjectAlreadyExistsException, ObjectNotFoundException, ForbiddenException
from unification import unify_external_namespaces


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
    def discover():
        # unify_external_namespaces()
        default = Namespace(Namespace.DEFAULT_NAMESPACE_NAME)
        result = execute_command('ip netns list')
        namespaces = [default] + [Namespace(name) for name in result.split()]
        return namespaces

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return '<' + self.name + '>'
