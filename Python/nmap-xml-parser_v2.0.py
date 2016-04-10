
import sys, argparse, os 
from xml.dom import minidom

__description__ = 'Nmap Parser'
__author__ = 'Sanoop Thomas a.k.a s4n7h0'
__version__ = '2.0'
__date__ = '23/05/2015'
__license__ = '(cc)Creative Commons 4.0'

class WRITE():

	count = 0
	def __init__(self,ofile):
		self.ofile = ofile 
		if self.ofile and self.ofile != '':
			self.output = open(self.ofile,'w')
		else:
			self.output = None

	def writeLine(self,line):
		self.count = self.count+1
		self.output.write(line + '\n')

	def close(self):
		print "\r\n" + str(self.count - 9 ) + " records saved \r\n"
		self.output.close()


class BuildCSV():

	def __init__(self,ofile):
		self.ofile = WRITE(ofile)
		self.delem = " ; "  # change this if you want to use other special char as delimiter 

	def banner(self):
		print "Nmap Parser v2.0"
		print "Author: Sanoop Thomas @s4n7h0"
		print "Version: 2.0"
		print "License: (cc)Creative Commons 4.0\r\n"

	def fetchElement(self,ifile,tag,elem):
		dom = minidom.parse(open(ifile, 'r'))
		self.tag = dom.getElementsByTagName(tag)
		return self.tag[0].getAttribute(elem)

	def header(self,fields):
		self.fields = fields.split('-')
		head = ""
		for f in self.fields:
			if head == '': head = f
			else: head = head + self.delem + f 
		self.ofile.writeLine(head)

	def parse(self,ifile,col):
		dom = minidom.parse(open(ifile,'r'))
		self.columns = col.split('-')
		host =""
		for hosts in dom.getElementsByTagName('host'):
			for ports in hosts.getElementsByTagName('port'):
				self.row = []
				row = ''
				if('start' in self.columns):
					start = self.fetchElement(ifile,'nmaprun','startstr') + self.delem
					self.row.append(start)
				if('end' in self.columns):
					end = self.fetchElement(ifile,'finished','timestr') + self.delem
					self.row.append(end)
				if('ip' in self.columns):
					for addr in hosts.getElementsByTagName('address'):
						if(addr.getAttribute('addrtype') == 'ipv4'):
							ip = addr.getAttribute('addr') + self.delem
							self.row.append(ip)
				if('host' in self.columns):
					for hostnames in hosts.getElementsByTagName('hostnames'):
						for hostname in hostnames.getElementsByTagName('hostname'):
							if(hostname.getAttribute('type') == 'user'):
								host = hostname.getAttribute('name') + self.delem
							else:
								host = " " + self.delem
						self.row.append(host)
				if('mac' in self.columns):
					for addr in hosts.getElementsByTagName('address'):
						if(addr.getAttribute('addrtype') == 'mac'):
							mac = addr.getAttribute('addr') + self.delem
						else:
							mac = " " + self.delem
						self.row.append(mac)
				if('vendor' in self.columns):
					for addr in hosts.getElementsByTagName('address'):
						if(addr.getAttribute('addrtype') == 'mac'):
							vendor = addr.getAttribute('vendor') + self.delem
						else:
							vendor = " " + self.delem
					self.row.append(vendor)
				if('port' in self.columns):
					port = ports.getAttribute('portid') + self.delem
					self.row.append(port)
				if('protocol' in self.columns):
					proto = ports.getAttribute('protocol') + self.delem
					self.row.append(proto)
				for states in ports.getElementsByTagName('state'):
					if('state' in self.columns):
						state = states.getAttribute('state') + self.delem
						self.row.append(state)
				for services in ports.getElementsByTagName('service'):
					if('service' in self.columns):
						service = services.getAttribute('name') + self.delem
						self.row.append(service)
					if('product' in self.columns):
						product = services.getAttribute('product') + self.delem
						self.row.append(product)
					if('version' in self.columns):
						version = services.getAttribute('version') + self.delem
						self.row.append(version)
					if('extrainfo' in self.columns):
						extrainfo = services.getAttribute('extrainfo') + self.delem
						self.row.append(extrainfo)
				if('script' in self.columns):
					script = []
					for scripts in ports.getElementsByTagName('script'):
						script.append(scripts.getAttribute('id') + ',')
					scriptlist = ''.join(script)
					self.row.append(scriptlist + self.delem)
				if('os' in self.columns):
					for oslist in hosts.getElementsByTagName('os'):
						for os in oslist.getElementsByTagName('osmatch'):
							osname = os.getAttribute('name') + self.delem
							self.row.append(osname)
				row = ''.join(map(str,self.row))
				self.ofile.writeLine(row)
		#self.ofile.close()

	def row(self,fields):
		print "writing row"

	def close():
		self.ofile.close()

def xml2csv(ifile,ofile,col):
	csv = BuildCSV(ofile)
	csv.banner()
	csv.header(col)
	csv.parse(ifile,col)

def xmls2csv(ifolder,ofile,col):
	csv = BuildCSV(ofile)
	csv.banner()
	csv.header(col)
	for xfile in os.listdir(ifolder):
		if xfile.endswith('.xml'):
			print("parsing " + xfile),
			csv.parse(ifolder+xfile,col)
			print(" >>> DONE")

def banner():
	banner = '''
                                                                        ____    ___  
 _ __  _ __ ___   __ _ _ __    _ __   __ _ _ __ ___  ___ _ __  __   __ |___ \  / _ \ 
| '_ \| '_ ` _ \ / _` | '_ \  | '_ \ / _` | '__/ __|/ _ \ '__| \ \ / /   __) || | | |
| | | | | | | | | (_| | |_) | | |_) | (_| | |  \__ \  __/ |     \ V /   / __/ | |_| |
|_| |_|_| |_| |_|\__,_| .__/  | .__/ \__,_|_|  |___/\___|_|      \_/   |_____(_)___/ 
                      |_|     |_|                                                    

	'''
	print banner

def main(argv):
	banner()
	
	parser = argparse.ArgumentParser(description='Parse Nmap xml files into csv format.')
	parser.add_argument("-i", "--input", dest="ifile", help="specify nmap xml output file as input.")
	parser.add_argument("-iF", "--inputFolfer", dest="ifolder", help="specify input list.")
	parser.add_argument("-o", "--output", dest="ofile", help="specify output file without extention.")
	parser.add_argument("-f", "--format", dest="format", default="csv", help="specify output file format.")
	parser.add_argument("-c", "--columns", dest="col", default="start-end-ip-host-mac-vendor-port-protocol-state-service-product-version-extrainfo-script-os", help="specify columns/fields that needs to be in output file")

	args = parser.parse_args()

	if args.format == 'csv' and args.ifile:
		xml2csv(args.ifile,args.ofile,args.col)
	elif args.format == 'csv' and args.ifolder:
		xmls2csv(args.ifolder,args.ofile,args.col)
	else:
		print "unknown output format."

if __name__ == '__main__':
	main(sys.argv)
	