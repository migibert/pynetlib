Feature: Manage namespace configurations
  In order to dynamically configure machines network configuration
  As a sysadmin or netadmin
  I want to manage namespace configurations from python scripts

  Scenario: Manage non existing namespaces creation
     Given namespace "creation" does not exist
     When I create a namespace "creation"
     Then namespace "creation" exists
     And no exception is raised

  Scenario: Manage existing namespaces creation
     Given namespace "creation" exists
     When I create a namespace "creation"
     Then an ObjectAlreadyExistsException is raised

  Scenario: Manage default namespace creation
     When I create the default namespace
     Then an ObjectAlreadyExistsException is raised

  Scenario: Manage existing namespaces deletion
     Given namespace "deletion" exists
     When I delete namespace "deletion"
     Then namespace "deletion" does not exist

  Scenario: Manage non existing namespaces deletion
     Given namespace "deletion" does not exist
     When I delete namespace "deletion"
     Then an ObjectNotFoundException is raised

  Scenario: Manage default namespace deletion
     When I delete the default namespace
     Then a ForbiddenException is raised

  Scenario: Manage namespace discovery
     Given namespace "namespace1" exists
     And namespace "namespace2" exists
     When I discover namespaces
     Then discovered namespaces contains "namespace1"
     And discovered namespaces contains "namespace2"
     And discovered namespaces contains default namespace