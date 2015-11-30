# pynetlib
[![Build Status](https://travis-ci.org/migibert/pynetlib.svg?branch=master)](https://travis-ci.org/migibert/pynetlib)
[![Coverage Status](https://coveralls.io/repos/migibert/pynetlib/badge.svg?branch=master&service=github)](https://coveralls.io/github/migibert/pynetlib?branch=master)
[![Code Climate](https://codeclimate.com/github/migibert/pynetlib/badges/gpa.svg)](https://codeclimate.com/github/migibert/pynetlib)
[![PyPI](https://img.shields.io/pypi/v/pynetlib.svg)](https://pypi.python.org/pypi/pynetlib)
[![License](http://img.shields.io/:license-mit-blue.svg)](http://doge.mit-license.org)  

[![PyPI](https://img.shields.io/pypi/dm/pynetlib.svg)](https://pypi.python.org/pypi/pynetlib)
[![PyPI](https://img.shields.io/pypi/dw/pynetlib.svg)](https://pypi.python.org/pypi/pynetlib)
[![PyPI](https://img.shields.io/pypi/dd/pynetlib.svg)](https://pypi.python.org/pypi/pynetlib)

## Features
This library is a toolbox to manipulate network configurations on Linux.

It supports:
- namespace discovery via `ip netns list`
- namespace creation via `ip netns add <namespace>`
- namespace deletion via `ip netns del <namespace>`
- device discovery via `ip addr list`
- address addition via `ip addr add <address> dev <device>`
- address deletion via `ip addr del <address> dev <device>`
- device ability via `ip link set <device> up`
- device disability via `ip link set <device> down`
- route discovery via `ip route list`
- route creation via `ip route add <destination> dev <device> via <gateway>`
- route deletion via `ip route del <destination>`

Make sure to run the scripts using this library with a user that can perform these operations.

## Namespaces
`ip netns` command only works with namespaces created with `ip netns add <namespace>` command. Namespaces created outside `ip` command (Docker, browsers, ...) are not manipulable this way.

However, as each process namespace is listed in `/proc/<pid>/ns/net` and `ip netns` works with `/var/run/netns`, pynetlib will create symlinks to make external namespaces manipulable with `ip` command. 

If the namespace does not exist anymore (because there is no more process that work with it), the symlink will be removed.

External namespaces keep their name : `net:[inode]`

## Installation
pynetlib is available on Pypi so it can be installed with pip: `pip install pynetlib`

## Development
You can run tests from project's root with the following commands:
- unit tests : ```py.test pynetlib --pep8 --cov=pynetlib --cov-report term-missing```
- functional tests : ```behave pynetlib/tests/specifications```

Dependencies can be intalled using test-requirements.txt file : ```pip install -r test-requirements.txt```

You may not want to play functional tests on your host as it changes eth2 configuration. If the device does not exist, tests will fail and, if it exists, it could break your device configuration (note that configurations are not persisted so a reboot will restore your host). 

A better place to play these tests is on a virtual machine and this is why a Vagrantfile is available so you can work on your host and run ```vagrant up``` which will :
- run a vm with virtualbox (so you need virtualbox to work this way)
- install your development version
- run functional tests

Feel free to submit pull request!

## Roadmap
Pynetlib's roadmap is defined via github issues and milestones.
