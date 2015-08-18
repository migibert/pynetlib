class ValueNotFoundException(Exception):
    def __init__(self, key):
        super(ValueNotFoundException, self).__init__('value not found for key %s' % key)


class ObjectAlreadyExistsException(Exception):
    def __init__(self, obj):
        super(ObjectAlreadyExistsException, self).__init__('Object %s already exists' % obj)


class ObjectNotFoundException(Exception):
    def __init__(self, obj):
        super(ObjectNotFoundException, self).__init__('Object %s does not exist' % obj)


class ForbiddenException(Exception):
    pass
