#sudo gedit /etc/ntp.conf 
#+: server 172.16.10.3
sudo /etc/init.d/ntp restart
sudo /etc/init.d/ntp stop
sudo ntpdate 172.16.10.3

