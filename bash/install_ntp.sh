sudo dpkg --configure -a
sudo apt-get update
sudo apt-get install ntp
sudo apt-get install ntpdate
sudo sh -c 'echo "server 172.16.10.3">>/etc/ntp.conf'
sudo /etc/init.d/ntp restart
sudo /etc/init.d/ntp stop
sudo ntpdate 172.16.10.3

