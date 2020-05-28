#!/usr/bin/python

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import *
import subprocess,json
import urllib,sys, getopt

# this script can be very well used to parse DNS record
# and do an intelligence recon on the relative records 
# such as IP address and geo location. It uses scapy
# to parse the pcap files and use www.hostip.info to 
# to recon the geo information.
# 
# this script can be used for post analysis of Fakenet
#
# Author : @s4n7h0 

 

def findDomains(pcap):
        #enumerating DNS records
	r=rdpcap(pcap)
        domain = set([])
        for i in range(0,len(r)):
                if((r[i][IP].proto)==17):
                        if(r[i][UDP].dport==53):
                                domain.add(r[i][UDP][DNSQR].qname[:-1])
        #gathering info using host
	ips = set([])
        for i in domain:
                try:
                        output=subprocess.check_output('host '+i+"| grep 'has address'", shell=True)
			if output and not output.isspace():
				ip = output.split('has address ')
        	                print i+" is up... doing further recon on this."
				findGeo(ip[1])                	    
                except subprocess.CalledProcessError as e:
                        output="host "+i+" is down"

def main(argv):
	pcap = ''
	banner()
	try:
		opts,args = getopt.getopt(argv,"hi:",["input="])
	except getopt.GetoptError:
		print "Invalid Argument ! Usage : python FindDomainCalls.py -i input.pcap"
		sys.exit(2)
	for opt,arg in opts:
		if opt == "-h":
			print "Usage : python FindDomainCalls.py -i input.pcap"
			sys.exit(0)
		elif opt in ("-i", "--input"):
			pcap = arg
		else:
			print "Usage : python FindDomainCalls.py -i input.pcap"
                        sys.exit(0)

	#loading pcap file
	findDomains(pcap)

def findGeo(ip):
	#enunmerating Geo Infomation
	geo = json.load(urllib.urlopen("http://api.hostip.info/get_json.php?ip="+ip))
	for item, value in geo.iteritems():
		print "\t\t"+item.strip() +": "+value.strip()
	
if __name__ == '__main__':
	main(sys.argv[1:])


