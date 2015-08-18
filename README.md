# pynet
[![Build Status](https://travis-ci.org/migibert/pynet.svg?branch=master)](https://travis-ci.org/migibert/pynet)
[![Coverage Status](https://coveralls.io/repos/migibert/pynet/badge.svg?branch=master)](https://coveralls.io/github/migibert/pynet)
[![License](http://img.shields.io/:license-mit-blue.svg)](http://doge.mit-license.org)  

This library is a wrapper around 'ip' command.

It supports:
- namespace discovery via `ip netns list`
- namespace creation via `ip netns add <namespace>`
- namespace deletion via `ip netns del <namespace>`
- device discovery via `ip addr list`
- address addition via `ip addr add <address> dev <device>`
- address deletion via `ip addr del <address> dev <device>`
- device ability via `ip link set <DEVICE> up`
- device disability via `ip link set <DEVICE> down`

Make sure to run the scripts using this library with a user that can perform these operations.

## Installation
Pynet is not yet available on Pypi so it has to be installed from git repo: `pip install git+https://github.com/migibert/pynet.git`

## Development
You can run tests from project's root with the following commands:
- unit tests : ```py.test pynet --pep8 --cov=pynet --cov-report term-missing```
- functional tests : ```behave pynet/tests/specifications```

Feel free to submit pull request!

##Roadmap
- List routes via `ip route show`
- Add static route via `ip route add <DESTINATION> via <GATEWAY> dev <DEVICE>`
- Remove static route via `ip route del <DESTINATION>`
- Add default gateway via `ip route add default via <GATEWAY>`
- Get broadcast addresses from `ip addr list`
- Get maximum transmission unit from `ip addr list`
- Get the length of the transmit queue from `ip addr list` (qlen field)
- Set the maximum transmission unit to device via `ip link set mtu <VALUE> dev <DEVICE>`
- Set the length of the transmit queue via `ip link set txqueuelen <LENGTH> dev <DEVICE>`
