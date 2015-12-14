from __future__ import absolute_import
from .utils import execute_command
from .exceptions import ObjectAlreadyExistsException, ObjectNotFoundException, ForbiddenException
from .unification import unify
import re


class Namespace():
    DEFAULT_NAMESPACE_NAME = ''

    def __init__(self, name):
        self.name = name if type(name) == str else name.decode('utf-8')
        self.devices = []

    def is_default(self):
        return self.name == Namespace.DEFAULT_NAMESPACE_NAME

    def is_external(self):
        pattern = re.compile('^net:\[([0-9])*\]$')
        return True if pattern.match(self.name) else False

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
        unify()
        default = Namespace(Namespace.DEFAULT_NAMESPACE_NAME)
        result = execute_command('ip netns list')
        namespaces = [default] + [Namespace(name) for name in result.split()]
        return namespaces

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return '<' + self.name + '>'
