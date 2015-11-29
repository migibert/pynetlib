Feature: Manage routes configurations
  In order to dynamically configure machines network routes
  As a sysadmin or netadmin
  I want to manage routes configurations from python scripts

  Scenario: Manage default route discovery
     When I discover routes
     Then "default" is found in discovered routes
     And no exception is raised

  Scenario: Manage routes discovery
     When I discover routes
     Then "10.0.0.0/16" is found in discovered routes
     And "10.0.2.0/24" is found in discovered routes
     And "172.17.100.0/24" is found in discovered routes
     And "192.168.100.0/24" is found in discovered routes
     And no exception is raised