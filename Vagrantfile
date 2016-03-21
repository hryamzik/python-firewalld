# -*- mode: ruby -*-
# vi: set ft=ruby :

defaultbox = "ubuntu/trusty64"
box = ENV['BOX'] || defaultbox

ENV['ANSIBLE_ROLES_PATH'] = "../"

Vagrant.configure(2) do |config|

  config.vm.box = box

  config.vm.define "python_firewalld" do |python_firewalld_cfg|
    python_firewalld_cfg.vm.hostname = "python.firewalld.vagrant"
    python_firewalld_cfg.vm.network "private_network", type: "dhcp"
    python_firewalld_cfg.vm.provider :virtualbox do |v|
      v.name = "python_firewalld"
    end
  end

  config.vm.provision :ansible do |ansible|
    ansible.playbook = "vagrant.yml"
    ansible.sudo = true
    ansible.groups = {
      "vagrant" => ["python_firewalld"],
    }
    ansible.extra_vars = {
      ansible_ssh_user: 'vagrant',
      hbase_standalone:   true,
    }

  end

end
