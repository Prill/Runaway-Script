#!/usr/bin/env python
# Copyright 2011,2012 Max W. Schwarz
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
 
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
print "Printing processes on <" + unicode(hostname) + ">" # with a minimum %CPU of", MINIMUM_PCPU
p = subprocess.Popen(['ps','--no-headers', '-eo','pcpu,pmem,pid,ruser,comm,etime,ni'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in p.stdout.readlines():
    stripped_line = line.strip()
    #print stripped_line
    m = re.match(r"^\W*(\d+\.\d+)",stripped_line)

    psData = re.match(r"^(?P<pcpu>\S+)\s+(?P<pmem>\S+)\s+(?P<pid>\S+)\s+(?P<ruser>\S+)\s+(?P<comm>\S+)\s+(?P<etime>\S+)\s+(?P<ni>\S+)",stripped_line)
    if psData:
        parsedData = {}
        parsedData["pcpu"] = float(psData.group("pcpu"))
        parsedData["pmem"] = float(psData.group("pmem"))
        parsedData["pid "] = int(psData.group("pid"))
        parsedData["ruser"] = psData.group("ruser")

        if parsedData["pcpu"] > MINIMUM_PCPU or parsedData["pmem"] > MINIMUM_PMEM:
            print "\t"+stripped_line
    else:
        print "Error: No data matched"
