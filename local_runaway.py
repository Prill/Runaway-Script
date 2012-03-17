#!/usr/bin/env python

import re
import subprocess

# The minimum PCPU value for the process to be considered "bad"
MINIMUM_PCPU = 10.0

# The minimum time the process can have been running for us to consider it a runaway (in minutes)
MINIMUM_TIME = 120 

# The minimum pmem (%)
MINIMUM_PMEM = 10.0


#print u"\u00bb"
hostname =  subprocess.Popen(["hostname", "-f"], stdout=subprocess.PIPE).stdout.read().strip()
print "Printing processes on <" + unicode(hostname)+ "> with a minimum %CPU of", MINIMUM_PCPU
p = subprocess.Popen(['ps','-eo', 'pcpu,pmem,pid,ruser,comm,etime,ni'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in p.stdout.readlines():
	stripped_line = line.strip()
	#print stripped_line
	m = re.match(r"^\W*(\d+\.\d+)",stripped_line)
	if m:
		pcpu = float(m.group(1))
		if pcpu > MINIMUM_PCPU:
			print "\t"+stripped_line

