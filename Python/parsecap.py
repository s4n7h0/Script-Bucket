#!/usr/bin/python
# this script will parse DNS records in a given pcap file and resolve the IP
# author : @s4n7h0

from scapy.all import *
import sys
import subprocess

argvs=sys.argv
argc=len(argvs)

#checking the right arguments
if(argc!=2):
	print 'Usage # pythion %s pcap_file'%argvs[0]
	quit()

#loading pcap file
r=rdpcap(argvs[1])
domain=set()

#enumerating DNS records
for i in range(0,len(r)):
	if((r[i][IP].proto)==17):
		if(r[i][UDP].dport==53):
			domain.add(r[i][UDP][DNSQR].qname[:-1])

#gathering info using host
for i in domain:
	try:
		output=subprocess.check_output('host '+i+"| grep 'has address'", shell=True)
	except subprocess.CalledProcessError as e:
		output="cant find host info"
	if output and not output.isspace():
		print "Gathering info of ",i
		print output
		print "======================================"
	
