# -*- coding: utf-8 -*-
#
# Copyright (C) 2007,2008,2011,2012 Red Hat, Inc.
#
# Authors:
# Thomas Woerner <twoerner@redhat.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import socket
import os.path
import shlex, pipes
from firewall.core.logger import log

def getPortID(port):
    """ Check and Get port id from port string or port id using socket.getservbyname

    @param port port string or port id
    @return Port id if valid, -1 if port can not be found and -2 if port is too big
    """
    
    if isinstance(port, int):
        id = port
    else:
        if port:
            port = port.strip()
        try:
            id = int(port)
        except:
            try:
                id = socket.getservbyname(port)
            except:
                return -1
    if id > 65535:
        return -2
    return id

def getPortRange(ports):
    """ Get port range for port range string or single port id

    @param ports an integer or port string or port range string
    @return Array containing start and end port id for a valid range or -1 if port can not be found and -2 if port is too big for integer input or -1 for invalid ranges or None if the range is ambiguous.
    """

    if isinstance(ports, int):
        id = getPortID(ports)
        if id >= 0:
            return (id,)
        return id

    splits = ports.split("-")
    matched = [ ]
    for i in xrange(len(splits), 0, -1):
        id1 = getPortID("-".join(splits[:i]))
        port2 = "-".join(splits[i:])
        if len(port2) > 0:
            id2 = getPortID(port2)
            if id1 >= 0 and id2 >= 0:
                if id1 < id2:
                    matched.append((id1, id2))
                elif id1 > id2:
                    matched.append((id2, id1))
                else:
                    matched.append((id1, ))
        else:
            if id1 >= 0:
                matched.append((id1,))
                if i == len(splits):
                    # full match, stop here
                    break
    if len(matched) < 1:
        return -1
    elif len(matched) > 1:
        return None
    return matched[0]

def portStr(port, delimiter=":"):
    """ Create port and port range string 
    
    @param port port or port range int or [int, int]
    @param delimiter of the output string for port ranges, default ':'
    @return Port or port range string, empty string if port isn't specified, None if port or port range is not valid
    """
    if port == "":
        return ""

    range = getPortRange(port)
    if isinstance(range, int) and range < 0:
        return None
    elif len(range) == 1:
        return "%s" % range
    else:
        return "%s%s%s" % (range[0], delimiter, range[1])

def getServiceName(port, proto):
    """ Check and Get service name from port and proto string combination using socket.getservbyport

    @param port string or id
    @param protocol string
    @return Service name if port and protocol are valid, else None
    """

    try:
        name = socket.getservbyport(int(port), proto)
    except:
        return None
    return name

def checkIP(ip):
    """ Check IPv4 address.
    
    @param ip address string
    @return True if address is valid, else False
    """

    try:
        socket.inet_pton(socket.AF_INET, ip)
    except socket.error as err:
        return False
    return True

def checkIP6(ip):
    """ Check IPv6 address.
    
    @param ip address string
    @return True if address is valid, else False
    """

    try:
        socket.inet_pton(socket.AF_INET6, ip)
    except socket.error as err:
        return False
    return True

def checkIPnMask(ip):
    if "/" in ip:
        addr = ip[:ip.index("/")]
        mask = ip[ip.index("/")+1:]
    else:
        addr = ip
        mask = None
    if not checkIP(addr):
        return False
    if mask:
        if "." in mask and checkIP(addr):
            return False
        else:
            try:
                i = int(mask)
            except:
                return False
            if i < 0 or i > 32:
                return False
    return True

def checkIP6nMask(ip):
    if "/" in ip:
        addr = ip[:ip.index("/")]
        mask = ip[ip.index("/")+1:]
    else:
        addr = ip
        mask = None
    if not checkIP6(addr):
        return False
    if mask:
        try:
            i = int(mask)
        except:
            return False
        if i < 0 or i > 128:
            return False

    return True

def checkProtocol(protocol):
    try:
        i = int(protocol)
    except:
        # string
        try:
            socket.getprotobyname(protocol)
        except:
            return False
    else:
        if i < 0 or i > 255:
            return False

    return True

def checkInterface(iface):
    """ Check interface string

    @param interface string
    @return True if interface is valid (maximum 16 chars and does not contain ' ', '/', '!', ':', '*'), else False
    """

    if not iface or len(iface) > 16:
        return False
    for ch in [ ' ', '/', '!', '*' ]:
        # !:* are limits for iptables <= 1.4.5
        if ch in iface:
            return False
    # disabled old iptables check
    #if iface == "+":
    #    # limit for iptables <= 1.4.5
    #    return False
    return True

def firewalld_is_active():
    """ Check if firewalld is active

    @return True if there is a firewalld pid file and the pid is used by firewalld
    """

    if not os.path.exists("/var/run/firewalld.pid"):
        return False

    try:
        with open("/var/run/firewalld.pid", "r") as fd:
            pid = fd.readline()
    except:
        return False

    if not os.path.exists("/proc/%s" % pid):
        return False

    try:
        with open("/proc/%s/cmdline" % pid, "r") as fd:
            cmdline = fd.readline()
    except:
        return False

    if "firewalld" in cmdline:
        return True

    return False

def readfile(filename):
    try:
        with open(filename, "r") as f:
            line = "".join(f.readlines())
    except Exception as e:
        log.error('Failed to read file "%s": %s' % (filename, e))
        return None
    return line

def writefile(filename, line):
    try:
        with open(filename, "w") as f:
            f.write(line)
    except Exception as e:
        log.error('Failed to write to file "%s": %s' % (filename, e))
        return False
    return True

def enable_ip_forwarding(ipv):
    if ipv == "ipv4":
        return writefile("/proc/sys/net/ipv4/ip_forward", "1\n")
    elif ipv == "ipv6":
        return writefile("/proc/sys/net/ipv6/conf/all/forwarding", "1\n")
    return False

def check_port(port):
    range = getPortRange(port)
    if range == -2 or range == -1 or range == None or \
            (len(range) == 2 and range[0] >= range[1]):
        if range == -2:
            log.debug2("'%s': port > 65535" % port)
        elif range == -1:
            log.debug2("'%s': port is invalid" % port)
        elif range == None:
            log.debug2("'%s': port is ambiguous" % port)
        elif len(range) == 2 and range[0] >= range[1]:
            log.debug2("'%s': range start >= end" % port)
        return False
    return True

def check_address(ipv, source):
    if ipv == "ipv4":
        if not checkIPnMask(source):
            return False
    elif ipv == "ipv6":
        if not checkIP6nMask(source):
            return False
    else:
        return False
    return True

def check_single_address(ipv, source):
    if ipv == "ipv4":
        if not checkIP(source):
            return False
    elif ipv == "ipv6":
        if not checkIP6(source):
            return False
    else:
        return False
    return True

def uniqify(input):
    # removes duplicates from list, whilst preserving order
    output = []
    for x in input:
        if x not in output:
            output.append(x)
    return output

def ppid_of_pid(pid):
    """ Get parent for pid """
    try:
        f = os.popen("ps -o ppid -h -p %d 2>/dev/null" % pid)
        pid = int(f.readlines()[0].strip())
        f.close()
    except:
        return None
    return pid

def max_zone_name_len():
    """
    Netfilter limits length of chain to (currently) 28 chars.
    The longest chain we create is FWDI_<zone>_allow,
    which leaves 28 - 11 = 17 chars for <zone>.
    """
    from firewall.core.base import SHORTCUTS
    longest_shortcut = max(map (len, SHORTCUTS.values()))
    return 28 - (longest_shortcut + len("__allow"))

def checkUser(user):
    if len(user) < 1 or len(user) > os.sysconf('SC_LOGIN_NAME_MAX'):
        return False
    return True

def checkUid(uid):
    if type(uid) == str:
        try:
            uid = int(uid)
        except:
            return False
    if uid > 0 or uid <= 2^31-1:
        return True
    return False

def checkCommand(command):
    if len(command) < 1 or len(command) > 1024:
        return False
    for ch in [ "|", "\n", "\0" ]:
        if ch in command:
            return False
    return True

def joinArgs(args):
    if "quote" in dir(shlex):
        return " ".join(shlex.quote(a) for a in args)
    else:
        return " ".join(pipes.quote(a) for a in args)

def splitArgs(string):
    return shlex.split(string)

def b2u(string):
    """ bytes to unicode """
    if isinstance(string, bytes):
        return string.decode('utf-8', 'replace')
    return string
