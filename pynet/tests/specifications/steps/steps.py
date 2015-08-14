from behave import given, when, then
from pynet.models import Namespace, Device
from pynet.exceptions import ObjectNotFoundException, ObjectAlreadyExistsException, ForbiddenException


@given(u'namespace "{namespace_name}" does not exist')
def step_impl(context, namespace_name):
    namespace = Namespace(namespace_name)
    if namespace in Namespace.discover():
        namespace.delete()

@given(u'namespace "{namespace_name}" exists')
def step_impl(context, namespace_name):
    namespace = Namespace(namespace_name)
    if namespace not in Namespace.discover():
        namespace.create()

@given(u'device "{device_name}" exists')
def step_impl(context, device_name):
    device = None
    for dev in Device.discover():
        if dev.name == device_name:
            device = dev
    assert device is not None

@given(u'address "{address}" does not exist on device "{device_name}"')
def step_impl(context, address, device_name):
    for dev in Device.discover():
        if dev.name == device_name and dev.contains_address(address):
            dev.remove_address(address)

@given(u'address "{address}" exists on device "{device_name}"')
def step_impl(context, address, device_name):
    for dev in Device.discover():
        if dev.name == device_name and not dev.contains_address(address):
            dev.add_address(address)

@given(u'device "{device_name}" is up')
def step_impl(context, device_name):
    for dev in Device.discover():
        if dev.name == device_name and not dev.is_up():
            dev.enable()

@given(u'device "{device_name}" is down')
def step_impl(context, device_name):
    for dev in Device.discover():
        if dev.name == device_name and not dev.is_down():
            dev.disable()

@when(u'I create a namespace "{namespace_name}"')
def step_impl(context, namespace_name):
    namespace = Namespace(namespace_name)
    try:
        namespace.create()
    except Exception as e:
        context.exception = e

@when(u'I create the default namespace')
def step_impl(context):
    namespace = Namespace('')
    try:
        namespace.create()
    except Exception as e:
        context.exception = e

@when(u'I delete namespace "{namespace_name}"')
def step_impl(context, namespace_name):
    namespace = Namespace(namespace_name)
    try:
        namespace.delete()
    except Exception as e:
        context.exception = e

@when(u'I delete the default namespace')
def step_impl(context):
    namespace = Namespace('')
    try:
        namespace.delete()
    except Exception as e:
        context.exception = e

@when(u'I discover namespaces')
def step_impl(context):
    context.discovered = Namespace.discover()

@when(u'I add address "{address}" to device "{device_name}"')
def step_impl(context, address, device_name):
    for dev in Device.discover():
        if dev.name == device_name:
            try:
                dev.add_address(address)
            except Exception as e:
                context.exception = e

@when(u'I remove address "{address}" from device "{device_name}"')
def step_impl(context, address, device_name):
    for dev in Device.discover():
        if dev.name == device_name:
            try:
                dev.remove_address(address)
            except Exception as e:
                context.exception = e

@when(u'I discover devices')
def step_impl(context):
    context.devices = Device.discover()

@when(u'I disable device "{device_name}"')
def step_impl(context, device_name):
    for dev in Device.discover():
        if dev.name == device_name:
            try:
                dev.disable()
            except Exception as e:
                context.exception = e

@when(u'I enable device "{device_name}"')
def step_impl(context, device_name):
    for dev in Device.discover():
        if dev.name == device_name:
            try:
                dev.enable()
            except Exception as e:
                context.exception = e

@then(u'namespace "{namespace_name}" exists')
def step_impl(context, namespace_name):
    namespace = Namespace(namespace_name)
    assert namespace.exists()

@then(u'namespace "{namespace_name}" does not exist')
def step_impl(context, namespace_name):
    namespace = Namespace(namespace_name)
    assert not namespace.exists()

@then(u'discovered namespaces contains "{namespace_name}"')
def step_impl(context, namespace_name):
    assert Namespace(namespace_name) in context.discovered

@then(u'discovered namespaces contains default namespace')
def step_impl(context):
    assert Namespace('') in context.discovered

@then(u'address "{address}" is affected to device "{device_name}"')
def step_impl(context, address, device_name):
    dev = None
    devices = Device.discover()
    for device in devices:
        if device.name == device_name:
            dev = device
            assert device.contains_address(address)
    assert dev is not None

@then(u'address {address}" is not affected to device "{device_name}"')
def step_impl(context, address, device_name):
    dev = None
    devices = Device.discover()
    for device in devices:
        if device.name == device_name:
            dev = device
            assert not device.contains_address(address)
    assert dev is not None

@then(u'"{device_name}" is found in discovered devices')
def step_impl(context, device_name):
    assert hasattr(context, 'devices')
    found = False
    for device in context.devices:
        if device_name == device.name:
            found = True
    assert found

@then(u'device "{device_name}" is down')
def step_impl(context, device_name):
    dev = None
    devices = Device.discover()
    for device in devices:
        if device.name == device_name:
            dev = device
            assert device.is_down()
    assert dev is not None

@then(u'device "{device_name}" is up')
def step_impl(context, device_name):
    dev = None
    devices = Device.discover()
    for device in devices:
        if device.name == device_name:
            dev = device
            assert device.is_up()
    assert dev is not None

@then(u'no exception is raised')
def step_impl(context):
    assert not hasattr(context, 'exception')

@then(u'an ObjectNotFoundException is raised')
def step_impl(context):
    assert isinstance(context.exception, ObjectNotFoundException)

@then(u'an ObjectAlreadyExistsException is raised')
def step_impl(context):
    assert isinstance(context.exception, ObjectAlreadyExistsException)

@then(u'a ForbiddenException is raised')
def step_impl(context):
    assert isinstance(context.exception, ForbiddenException)
