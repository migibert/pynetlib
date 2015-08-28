# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu-precise_14.04_x64"
  config.vm.box_url = "https://oss-binaries.phusionpassenger.com/vagrant/boxes/latest/ubuntu-14.04-amd64-vbox.box"

  config.vm.define "pynetlib" do |pynetlib|
    pynetlib.vm.network "private_network", ip: "192.168.100.100"
    pynetlib.vm.network "private_network", ip: "172.17.100.100"

    pynetlib.vm.provider :virtualbox do |vb|
      vb.name = "pynetlib"
      vb.customize ["modifyvm", :id, "--cpus", "1"]
      vb.customize ["modifyvm", :id, "--memory", "256"]
    end
  end

  config.vm.provision :shell, :inline => "apt-get update"
  config.vm.provision :shell, :inline => "apt-get install -y docker.io && ln -sf /usr/bin/docker.io /usr/local/bin/docker"
  config.vm.provision :shell, :inline => "apt-get install -y python-pip"
  config.vm.provision :shell, :inline => "pip install -r /vagrant/requirements.txt"
  config.vm.provision :shell, :inline => "pip install -r /vagrant/test-requirements.txt"
  config.vm.provision :shell, :inline => "pip install -e /vagrant"
  config.vm.provision :shell, :inline => "behave /vagrant/pynetlib/tests/specifications"
end
