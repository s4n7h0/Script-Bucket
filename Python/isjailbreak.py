#!/usr/bin/python

import os,sys,getopt

__description__ = 'Jailbreak Detection Patch using basic file search escape. Use this at own risks as this script is dirty as it is coded. Replacing files might cause issues on the device. Advice to keep a track of all changes that this script is making on execution.'
__author__ = 'Sanoop Thomas a.k.a @s4n7h0'
__version__ = '1.0'
__date__ = '22/12/2015'


files=["/private/var/stash",
		"/private/var/lib/apt",
		"/private/var/tmp/cydia.log",
		"/private/var/lib/cydia",
		"/private/var/mobile/Library/SBSettings/Themes",
		"/Library/MobileSubstrate/MobileSubstrate.dylib",
		"/Library/MobileSubstrate/DynamicLibraries/Veency.plist",
		"/Library/MobileSubstrate/DynamicLibraries/LiveClock.plist",
		"/System/Library/LaunchDaemons/com.ikey.bbot.plist",
		"/System/Library/LaunchDaemons/com.saurik.Cydia.Startup.plist",
		"/var/cache/apt",
		"/var/lib/apt",
		"/var/lib/cydia",
		"/var/log/syslog",
		"/var/tmp/cydia.log",
		"/bin/bash",
		"/bin/sh",
		"/usr/sbin/sshd",
		"/usr/libexec/ssh-keysign",
		"/usr/sbin/sshd",
		"/usr/bin/sshd",
		"/usr/libexec/sftp-server",
		"/etc/ssh/sshd_config",
		"/etc/apt",
		"/Applications/Cydia.app",
		"/Applications/RockApp.app",
		"/Applications/Icy.app",
		"/Applications/WinterBoard.app",
		"/Applications/SBSettings.app",
		"/Applications/MxTube.app",
		"/Applications/IntelliScreen.app",
		"/Applications/FakeCarrier.app",
		"/Applications/blackra1n.app"]
prefix = 'isjail_'
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
NOTFOUND = '\033[91m'
ENDC = '\033[0m'
BOLD = "\033[1m"

def found(msg,filename):
    	print OKGREEN + msg + ENDC + " : " + filename

def warn(msg,filename):
    print WARNING + msg + ENDC + " " + filename

def notfound(msg,filename):
    print NOTFOUND + msg + ENDC + " " + filename

def patch():
	for f in files:
		if(os.path.exists(f)):
			found('Found',f)
			# If file found, then patch it with isjail_ prefix
			path,filename=os.path.split(f)
			newpath=os.path.join(path,(prefix+filename))	
			os.rename(f, newpath)
			warn('  - Patched to ',newpath)
		else:
			notfound('Not found ',f)
	return
	print "You may need to manually restore /private/var/stash before running restore command"

def restore():
	for f in files:
		tpath,tf = os.path.split(f)
		newtpath = os.path.join(tpath,(prefix+tf))
		# If file found, then restore it
		if(os.path.exists(newtpath)):
			found('Found',tf)
			path,filename=os.path.split(newtpath)
			os.rename(newtpath,f)
			warn(' - Restored to ',f)
		else:
			notfound('Not Found ',newtpath)
 	return 

def usage():
	usage = """
		help	prints this 
		patch	find and patch the file  with prefix 'isjail_
		restore	restore files 
		"""
	print "python isjailbreak.py [patch|restore]"
	print usage

def main(argv):
	
	try:
    		opts, args = getopt.getopt(sys.argv[1:], 'm:p:h', ['patch', 'restore', 'help'])
	except getopt.GetoptError:
    		usage()
    		sys.exit(2)

	for arg in args:
		if arg  == 'patch':
			patch()
		elif arg == 'restore':
			restore()
		else:
			print "Wrong Argument !\n"
			usage()
			sys.exit(2)


if __name__ == "__main__":
	main(sys.argv[1:])
