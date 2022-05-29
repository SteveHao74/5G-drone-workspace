route -n
sudo route del default gw 192.168.2.1
sudo route add default gw 192.168.2.1 dev wlan0
