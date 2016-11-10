#!/usr/bin/env python2

"""
python2 instead of pythong for portability concerns. See link
    https://www.python.org/dev/peps/pep-0394/
"""


import json
import sys
import subprocess
import tempfile
import re
import platform
import requests

#
#Define os specific way of handling regex capture
#
#   These functions all accept a captures tuple
#   And return a captures tuple
#
#   Their goal is to re-rder/manipluate the contents
#   so the output json is consisentent
#
def windows_captures(x):
    return x
def linux_captures(x):
    return (x[2]+x[3],x[4],x[5])


#
#Define os specific way of pulling network data
#
#   These functions all accept 2 files
#   And return 2 files
#
#   They allow individual OS's to to specify their own method
#   of fetching data
#
def win_cmd(out,err):
    subprocess.call(["ipconfig","/all"],
            shell = True,
            stdout = out,
            stderr = err,
            bufsize = -1)
    return (out,err)

def lnx_cmd(out,err):
    subprocess.call(["ifconfig"],
            shell = True,
            stdout = out,
            stderr = err,
            bufsize = -1)
    subprocess.call(["netstat -nr"],
            shell = True,
            stdout = out,
            stderr = err,
            bufsize = -1)
    return(out,err)
#
#Define all the OS specific stuff in a dictionary ahead of time
#
#   Defines:
#       cmd: A function to pull the system data
#       reg: The regular expression to capture data
#       lambda: A function to order the data
#
#   Supported Platforms:
#       Linux
#       Windows
#
os_specific = {
    'Windows': {
        'cmd': win_cmd,
        'reg': r"(?:Connection|Network|Ethernet\d*)\s*\d*:\s*Connection-specific DNS Suffix[ \.]+:[\s\S]*?IPv4 Address[ \.]+:\s*([\d\.]{7,15})[\s\S]*?Subnet Mask[ \.]+:\s*([\d\.]{7,15})[\s\S]*?Default Gateway[ \.]+:\s*([\d\.]{7,15})",
        'lambda': windows_captures
        },
    'Linux': {
        'cmd': lnx_cmd,
        'reg': r"(?P<iface>\w+)\s*Link encap:\w+\s*HWaddr (?P<mac>[a-f\d:]{17})\s*inet addr:(?P<ipv4>\d{1,3}\.\d{1,3}\.)(\d{1,3}\.\d{1,3})[\s\S]*?Mask:(?P<subnet>[\d\.]{7,15})[\s\S]*?0\.0\.0\.0\s*((?P=ipv4)\d{1,3}\.\d{1,3})\s*0\.0\.0\.0\s*\w+\s*\d*\s*\d*\s*\d*\s*(?P=iface)[\s\S]*?(?P=ipv4)\d{1,3}\.\d{1,3}\s*0\.0\.0\.0\s*(?P=subnet)\s*\w+\s*\d*\s*\d*\s*\d*\s*(?P=iface)",
        'lambda': linux_captures
        },
}



#
#Get platforom specific data
#
#   Calls into os_specific dictionary
#
def os_details():
    name = platform.uname()[0]
    dic = os_specific[name]
    reg = re.compile(dic['reg'])
    return (dic['cmd'],reg,dic['lambda'])



#
#Run a shell command in a platform agnostic way
#
#   This will create 2 temporary files for STDOUT, and STDERR
#   Windows doesn't support pipes
#   Unix does support temp files
#   Usage of shell is unsafe on Unix, but manditory on Unix.
#
def run_cmd(cmd_let):

    """Make temp files"""
    err = tempfile.NamedTemporaryFile()
    out = tempfile.NamedTemporaryFile()

    """Call into Shell"""
    (out, err) = cmd_let(out,err)

    out.flush()
    out.seek(0,0)
    err.flush()
    err.seek(0,0)

    stdin = err.read().strip()

    """Check if stdin has data. If so return it instead of stdout"""
    if len(stdin) > 0:
        return (1,stdin)
    else:
        return (0,out.read().strip())



#
#Parse command
#
#   Accepts Regex + STDOUT will return IPv4, Machine Addr,
#
#   Only supports 1 interface per host
#
def parse_data(buf,reg,func):
    return list(map(func,reg.findall(buf)))



#
#The main routine
#
#   ENTRY POINT
#
def entry_point():

    """Host Specific Details"""
    (cmdlet,regex, func) = os_details()

    """Execute the shell command, capture output"""
    (err,stdout) = run_cmd( cmdlet )
    if err != 0:
        print "Error detecting OS interface configuration"
        print "Error code %d"%(err)
        print stdout
        sys.exit(1)

    """Parse shell command output"""
    interfaces = parse_data(stdout,regex, func)
    if len(interfaces) == 0:
        print "No interfaces found"
        sys.exit(1)

    """Configure to final form"""
    output = {
        'host': platform.uname()[1],
        'interfaces': interfaces
    }

    """Send data to server"""
    requests.post(sys.argv[1],data=json.dumps(output))




if __name__ == "__main__":
    entry_point()
