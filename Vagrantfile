# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

IP = "10.42.2.100"
SSH_PORT = 2232
MEMORY = 1024
NAME = "api.opencivicdata.org"
FOLDERS = {"/projects/ocdapi/src/api" => ".",
           "/projects/ocdapi/src/imago" => "../imago"
          }

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "chef/ubuntu-13.10"

  # awkward fix for SSH reassignment issue (re-evaluate w/ Vagrant 1.5.4)
  config.vm.network :forwarded_port, guest: 22, host: 2222, id: "ssh", disabled: true
  config.vm.network :forwarded_port, guest: 22, host: SSH_PORT, auto_correct: true

  # assign a private IP
  config.vm.network "private_network", ip: IP

  FOLDERS.each do |dest, src|
      config.vm.synced_folder src, dest
  end

  config.vm.provider "virtualbox" do |v|
    v.memory = MEMORY
    v.name = NAME
  end

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "ansible/site.yml"
    ansible.inventory_path = "ansible/hosts.vagrant"
    ansible.limit = "all"
    # needed for common tasks to avoid EBS & checkout over synced_folders
    ansible.extra_vars = { deploy_type: "vagrant" }
    # seems to avoid the delay with private IP not being available
    ansible.raw_arguments = ["-T 30"]
  end
end
