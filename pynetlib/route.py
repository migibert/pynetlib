from __future__ import absolute_import
from .utils import execute_command, get_routes_info
from .exceptions import ObjectNotFoundException, ObjectAlreadyExistsException
from . import NetworkBase


class Route(NetworkBase):
    def __init__(self, destination, device, namespace=None):
        self.destination = destination
        self.device = device
        self.gateway = None
        self.source = None
        self.scope = None
        self.metric = None
        self.prohibited = False
        self.reachable = True
        self.namespace = namespace

    def is_default(self):
        return self.destination == 'default'

    def is_prohibited(self):
        return self.prohibited

    def is_reachable(self):
        return self.reachable

    @staticmethod
    def discover(namespace=None):
        routes = []
        output = execute_command('ip route list', namespace=namespace)
        for destination, device, metric, scope, gateway, source, prohibited, reachable in get_routes_info(output):
            route = Route(destination, device, namespace=namespace)
            route.metric = metric
            route.gateway = gateway
            route.source = source
            route.scope = scope
            route.prohibited = prohibited
            route.reachable = reachable
            routes.append(route)
        return routes

    def refresh(self):
        routes = Route.discover(namespace=self.namespace)
        if self not in routes:
            raise ObjectNotFoundException(self)
        found = routes[routes.index(self)]
        self.metric = found.metric
        self.gateway = found.gateway
        self.source = found.source
        self.scope = found.scope
        self.prohibited = found.prohibit
        self.reachable = found.reachable

    def create(self):
        if self.exists():
            raise ObjectAlreadyExistsException(self)
        gatewaycmd = '' if self.gateway is None else 'via %s' % self.gateway
        cmd = 'ip route add %s dev %s %s' % (self.destination, self.device, gatewaycmd)
        execute_command(cmd, namespace=self.namespace)

    def delete(self):
        if not self.exists():
            raise ObjectNotFoundException(self)
        execute_command('ip route del %s' % self.destination, namespace=self.namespace)

    def prohibit(self):
        if self.exists():
            raise ObjectAlreadyExistsException(self)
        execute_command('ip route add prohibit %s' % self.destination, namespace=self.namespace)

    def unreachable(self):
        if self.exists():
            raise ObjectAlreadyExistsException(self)
        execute_command('ip route add unreachable %s' % self.destination, namespace=self.namespace)

    def exists(self):
        return self in Route.discover(self.namespace)

    def __eq__(self, other):
        return self.destination == other.destination
