# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.hostname = "sampleapp.example.com"

  config.vm.provider :virtualbox do |vb, override|
    vb.customize ["modifyvm", :id, "--memory", "1024"]
    override.vm.box = "centos65-x86_64-20131205.box"
    override.vm.box_url = "https://github.com/2creatives/vagrant-centos/releases/download/v6.5.1/centos65-x86_64-20131205.box"
    override.vm.provision :shell, :path => "setup_centos.sh"    
    override.vm.network "forwarded_port", guest: 80, host: 8080
  end

end
