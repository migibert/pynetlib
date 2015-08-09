# pynet
[![Build Status](https://travis-ci.org/migibert/pynet.svg?branch=master)](https://travis-ci.org/migibert/pynet)

This library is a wrapper around 'ip' command. 

It supports:
- namespace discovery via `ip netns list`
- device discovery (inside or outside namespaces) via `ip addr list`

## Installation
Pynet is not yet available on Pypi so it has to be installed from git repo: `pip install git+https://github.com/migibert/pynet.git`

## Development
You can run tests with ```py.test --pep8 pynet```

##Roadmap
- Enable network interface via `ip link set <DEVICE> up`
- Disable network interface via `ip link set <DEVICE> down`
- List routes via `ip route show`
- Add static route via `ip route add <DESTINATION> via <GATEWAY> dev <DEVICE>`
- Remove static route via `ip route del <DESTINATION>`
- Add default gateway via `ip route add default via <GATEWAY>`
