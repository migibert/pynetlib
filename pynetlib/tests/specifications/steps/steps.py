from __future__ import absolute_import
import subprocess
from behave import given, when, then
from pynetlib.device import Device
from pynetlib.namespace import Namespace
from pynetlib.exceptions import ObjectNotFoundException, ObjectAlreadyExistsException, ForbiddenException


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
    assert device is not None   # TODO: create the device if necessary
    context.device = device


@given(u'address "{address}" does not exist on device "{device_name}"')
def step_impl(context, address, device_name):
    for dev in Device.discover():
        if dev.name == device_name and dev.contains_address(address):
            dev.remove_address(address)
            context.device = dev


@given(u'address "{address}" exists on device "{device_name}"')
def step_impl(context, address, device_name):
    for dev in Device.discover():
        if dev.name == device_name and not dev.contains_address(address):
            dev.add_address(address)
            context.device = dev


@given(u'device "{device_name}" is up')
def step_impl(context, device_name):
    for dev in Device.discover():
        if dev.name == device_name and not dev.is_up():
            dev.enable()
            context.device = dev


@given(u'device "{device_name}" is down')
def step_impl(context, device_name):
    for dev in Device.discover():
        if dev.name == device_name and not dev.is_down():
            dev.disable()
            context.device = dev


@given(u'at least one docker container is running')
def step_impl(context):
    output = subprocess.check_output('docker ps', shell=True)
    lines = [line for line in output.split('\n') if line]
    if len(lines) <= 1:
        subprocess.check_output('docker run -d -t progrium/busybox', shell=True)


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
    device = context.device
    assert device.name == device_name
    try:
        device.add_address(address)
    except Exception as e:
        context.exception = e


@when(u'I remove address "{address}" from device "{device_name}"')
def step_impl(context, address, device_name):
    device = context.device
    assert device.name == device_name
    try:
        device.remove_address(address)
    except Exception as e:
        context.exception = e


@when(u'I discover devices')
def step_impl(context):
    context.devices = Device.discover()


@when(u'I disable device "{device_name}"')
def step_impl(context, device_name):
    device = context.device
    assert device.name == device_name
    try:
        device.disable()
    except Exception as e:
        context.exception = e


@when(u'I enable device "{device_name}"')
def step_impl(context, device_name):
    device = context.device
    assert device.name == device_name
    try:
        device.enable()
    except Exception as e:
        context.exception = e


@when(u'I remove all docker containers')
def step_impl(context):
    subprocess.check_output('docker stop $(docker ps -a -q)', shell=True)


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
    device = context.device
    assert device.name == device_name
    assert device.contains_address(address)


@then(u'address {address}" is not affected to device "{device_name}"')
def step_impl(context, address, device_name):
    device = context.device
    assert device.name == device_name
    assert not device.contains_address(address)


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
    device = context.device
    assert device.name == device_name
    assert device.is_down()


@then(u'device "{device_name}" is up')
def step_impl(context, device_name):
    device = context.device
    assert device.name == device_name
    assert device.is_up()


@then(u'an external namespace exists')
def step_impl(context):
    external_namespaces = [ns for ns in context.discovered if ns.is_external()]
    assert len(external_namespaces) > 0


@then(u'no external namespace exists')
def step_impl(context):
    external_namespaces = [ns for ns in context.discovered if ns.is_external()]
    assert len(external_namespaces) == 0


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
