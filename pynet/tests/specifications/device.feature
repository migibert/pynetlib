Feature: Manage devices configurations
  In order to dynamically configure machines network configuration
  As a sysadmin or netadmin
  I want to manage devices configurations from python scripts

  Scenario: Manage non existing address addition
     Given device "eth0" exists
     And address "172.16.10.10/32" does not exist on device "eth0"
     When I add address "172.16.10.10/32" to device "eth0"
     Then address "172.16.10.10/32" is affected to device "eth0"
     And no exception is raised

  Scenario: Manage existing address addition
     Given device "eth0" exists
     And address "172.16.10.10/32" exists on device "eth0"
     When I add address "172.16.10.10/32" to device "eth0"
     Then an ObjectAlreadyExistsException is raised

  Scenario: Manage existing address deletion
     Given device "eth0" exists
     And address "172.16.10.10/32" exists on device "eth0"
     When I remove address "172.16.10.10/32" from device "eth0"
     Then address "172.16.10.10/32" is not affected to device "eth0"
     And no exception is raised

  Scenario: Manage non existing address deletion
     Given device "eth0" exists
     And address "172.16.10.10/32" does not exist on device "eth0"
     When I remove address "172.16.10.10/32" from device "eth0"
     Then an ObjectNotFoundException is raised

  Scenario: Manage device discovery
     When I discover devices
     Then "lo" is found in discovered devices
     And "eth0" is found in discovered devices
     And no exception is raised

  Scenario: Manage device deactivation
     Given device "eth0" exists
     And device "eth0" is up
     When I disable device "eth0"
     Then device "eth0" is down
     And no exception is raised

    Scenario: Manage device activation
     Given device "eth0" exists
     And device "eth0" is down
     When I enable device "eth0"
     Then device "eth0" is up
     And no exception is raised