from __future__ import absolute_import
import inspect


class NetworkBase():
    def __repr__(self):
        members = inspect.getmembers(self, lambda a: not(inspect.isroutine(a)))
        attributes = [a for a in members if '_' not in a[0]]
        result = ', '.join(['%s=%s' % (key, value) for key, value in attributes])
        return '<' + result + '>'
