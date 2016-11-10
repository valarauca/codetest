#!/usr/bin/env python2
""""
python2 instead of python for portability concerns. See link

    https://www.python.org/dev/peps/pep-0394/
"""

import re
import unittest
import if_client


linux_validation_data ="""
eth0      Link encap:Ethernet  HWaddr 1a:15:3d:88:ed:e2
          inet addr:159.203.58.254  Bcast:159.203.63.255  Mask:255.255.248.0
          inet6 addr: fe80::1815:3dff:fe88:ede2/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:820345 errors:0 dropped:0 overruns:0 frame:0
          TX packets:442419 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:739246639 (739.2 MB)  TX bytes:73706958 (73.7 MB)

eth1      Link encap:Ethernet  HWaddr 36:26:a9:96:53:26
          inet6 addr: fe80::3426:a9ff:fe96:5326/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:7 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:0 (0.0 B)  TX bytes:578 (578.0 B)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:160 errors:0 dropped:0 overruns:0 frame:0
          TX packets:160 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1
          RX bytes:11840 (11.8 KB)  TX bytes:11840 (11.8 KB)

Kernel IP routing table
Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
0.0.0.0         159.203.56.1    0.0.0.0         UG        0 0          0 eth0
10.20.0.0       0.0.0.0         255.255.0.0     U         0 0          0 eth0
159.203.56.0    0.0.0.0         255.255.248.0   U         0 0          0 eth0

"""

windows_validation_data ="""

Windows IP Configuration

   Host Name . . . . . . . . . . . . : LaederW
   Primary Dns Suffix  . . . . . . . :
   Node Type . . . . . . . . . . . . : Hybrid
   IP Routing Enabled. . . . . . . . : No
   WINS Proxy Enabled. . . . . . . . : No
   DNS Suffix Search List. . . . . . :

Ethernet adapter Bluetooth Network Connection 3:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . :
   Description . . . . . . . . . . . : Bluetooth Device (Personal Area Network) #3
   Physical Address. . . . . . . . . : 08-3E-8E-A0-3D-A2
   DHCP Enabled. . . . . . . . . . . : Yes
   Autoconfiguration Enabled . . . . : Yes

Wireless LAN adapter Wireless Network Connection 3:

   Connection-specific DNS Suffix  . :
   Description . . . . . . . . . . . : Broadcom BCM943228HM4L 802.11a/b/g/n 2x2 WiFi Adapter #3
   Physical Address. . . . . . . . . : A4-17-31-59-5A-CB
   DHCP Enabled. . . . . . . . . . . : Yes
   Autoconfiguration Enabled . . . . : Yes
   IPv4 Address. . . . . . . . . . . : 10.228.53.107(Preferred)
   Subnet Mask . . . . . . . . . . . : 255.255.254.0
   Lease Obtained. . . . . . . . . . :
   Lease Expires . . . . . . . . . . :
   Default Gateway . . . . . . . . . : 10.228.52.1
   DHCP Server . . . . . . . . . . . : 1.1.1.1
   DNS Servers . . . . . . . . . . . : 10.228.52.28
                                       10.228.52.25
   NetBIOS over Tcpip. . . . . . . . : Enabled

Ethernet adapter Local Area Connection:

   Connection-specific DNS Suffix  . :
   Description . . . . . . . . . . . : Intel(R) 82579V Gigabit Network Connection
   Physical Address. . . . . . . . . : 6C-3B-E5-F5-30-85
   DHCP Enabled. . . . . . . . . . . : Yes
   Autoconfiguration Enabled . . . . : Yes
   Autoconfiguration IPv4 Address. . : 169.254.60.205(Preferred)
   Subnet Mask . . . . . . . . . . . : 255.255.0.0
   Default Gateway . . . . . . . . . :
   NetBIOS over Tcpip. . . . . . . . : Enabled

Ethernet adapter VirtualBox Host-Only Network:

   Connection-specific DNS Suffix  . :
   Description . . . . . . . . . . . : VirtualBox Host-Only Ethernet Adapter
   Physical Address. . . . . . . . . : 0A-00-27-00-00-00
   DHCP Enabled. . . . . . . . . . . : No
   Autoconfiguration Enabled . . . . : Yes
   Link-local IPv6 Address . . . . . : fe80::7d7e:d746:4b03:589e%21(Preferred)
   IPv4 Address. . . . . . . . . . . : 192.168.56.1(Preferred)
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . :
   DHCPv6 IAID . . . . . . . . . . . : 470417447
   DHCPv6 Client DUID. . . . . . . . : 00-01-00-01-1E-60-D6-47-6C-3B-E5-F5-30-85
   DNS Servers . . . . . . . . . . . : fec0:0:0:ffff::1%1
                                       fec0:0:0:ffff::2%1
                                       fec0:0:0:ffff::3%1
   NetBIOS over Tcpip. . . . . . . . : Enabled

Tunnel adapter isatap.{6C795D30-FD5A-4AB0-AF51-0E6EAED76579}:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . :
   Description . . . . . . . . . . . : Microsoft ISATAP Adapter
   Physical Address. . . . . . . . . : 00-00-00-00-00-00-00-E0
   DHCP Enabled. . . . . . . . . . . : No
   Autoconfiguration Enabled . . . . : Yes

Tunnel adapter isatap.det.meaa.local:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . :
   Description . . . . . . . . . . . : Microsoft ISATAP Adapter #2
   Physical Address. . . . . . . . . : 00-00-00-00-00-00-00-E0
   DHCP Enabled. . . . . . . . . . . : No
   Autoconfiguration Enabled . . . . : Yes

Tunnel adapter isatap.{BA7D96DF-A171-4536-85F2-DAFCB81F55D5}:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . :
   Description . . . . . . . . . . . : Microsoft ISATAP Adapter #3
   Physical Address. . . . . . . . . : 00-00-00-00-00-00-00-E0
   DHCP Enabled. . . . . . . . . . . : No
   Autoconfiguration Enabled . . . . : Yes

Tunnel adapter isatap.{6B6D5160-4C9C-4EA1-AC24-8F2723E52554}:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . :
   Description . . . . . . . . . . . : Microsoft ISATAP Adapter #4
   Physical Address. . . . . . . . . : 00-00-00-00-00-00-00-E0
   DHCP Enabled. . . . . . . . . . . : No
   Autoconfiguration Enabled . . . . : Yes

"""


windows_validation_2 = """

Windows IP Configuration

   Host Name . . . . . . . . . . . . : DETMYSQL01
   Primary Dns Suffix  . . . . . . . :
   Node Type . . . . . . . . . . . . : Hybrid
   IP Routing Enabled. . . . . . . . : No
   WINS Proxy Enabled. . . . . . . . : No
   DNS Suffix Search List. . . . . . :

Ethernet adapter Ethernet0 2:

   Connection-specific DNS Suffix  . :
   Description . . . . . . . . . . . : vmxnet3 Ethernet Adapter
   Physical Address. . . . . . . . . : 00-50-56-B8-F9-A8
   DHCP Enabled. . . . . . . . . . . : No
   Autoconfiguration Enabled . . . . : Yes
   IPv4 Address. . . . . . . . . . . : 10.228.53.219(Preferred)
   Subnet Mask . . . . . . . . . . . : 255.255.254.0
   Default Gateway . . . . . . . . . : 10.228.52.1
   DNS Servers . . . . . . . . . . . : 10.228.52.28
                                       10.228.52.25
   NetBIOS over Tcpip. . . . . . . . : Enabled

Tunnel adapter isatap.{B5CA0564-127C-4E6E-851A-F283B04CFC2B}:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . :
   Description . . . . . . . . . . . : Microsoft ISATAP Adapter #2
   Physical Address. . . . . . . . . : 00-00-00-00-00-00-00-E0
   DHCP Enabled. . . . . . . . . . . : No
   Autoconfiguration Enabled . . . . : Yes

Tunnel adapter Teredo Tunneling Pseudo-Interface:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . :
   Description . . . . . . . . . . . : Microsoft Teredo Tunneling Adapter
   Physical Address. . . . . . . . . : 00-00-00-00-00-00-00-E0
   DHCP Enabled. . . . . . . . . . . : No
   Autoconfiguration Enabled . . . . : Yes

"""


class TestObject(unittest.TestCase):

    #
    #ensure windows captures method does no re-ordering
    #
    def test_windows_captures(self):
        tup = ("Foo", "Bar", "Hello World!")
        dut = if_client.windows_captures(tup)
        self.assertEqual( tup, dut)

        """there is an alterate way that interface is exposed"""
        tup = ("Foo", "Bar", "Hello World!")
        dut = if_client.os_specific['Windows']['lambda'](tup)
        self.assertEqual( tup, dut)


    #
    #Ensure the linux drops first 2, and combines 3/4, passed rest
    #
    def test_linux_captures(self):
        tup = ("Drop1","Drop2","Foo","Bar","Hello","World")
        dut = if_client.linux_captures(tup)
        out = ("FooBar", "Hello", "World")
        self.assertEqual(dut,out)

        """there is an alterate way that interface is exposed"""
        tup = ("Drop1","Drop2","Foo","Bar","Hello","World")
        dut = if_client.os_specific['Linux']['lambda'](tup)
        out = ("FooBar", "Hello", "World")
        self.assertEqual(dut,out)

    #
    #Valid Windows regex
    #
    def test_win_regex(self):
        windows_regex = if_client.os_specific['Windows']['reg']
        regex = re.compile(windows_regex)
        data = regex.findall(windows_validation_data )

        """we should capture something"""
        self.assertTrue( len(data) > 0 )
        tup = data[0]

        """we should capture 3 things actually"""
        self.assertTrue( len(tup) == 3 )

        """thing 0 is the IP address"""
        self.assertEqual( tup[0], '10.228.53.107')

        """thing 1 is the net mask"""
        self.assertEqual( tup[1], '255.255.254.0')

        """thing 1 is the gateway"""
        self.assertEqual( tup[2], '10.228.52.1')

    #
    #Valid Windows regex
    #
    def test_win_regex(self):
        windows_regex = if_client.os_specific['Windows']['reg']
        regex = re.compile(windows_regex)
        data = regex.findall(windows_validation_2 )

        """we should capture something"""
        self.assertTrue( len(data) > 0 )
        tup = data[0]

        """we should capture 3 things actually"""
        self.assertTrue( len(tup) == 3 )

        """thing 0 is the IP address"""
        self.assertEqual( tup[0], '10.228.53.219')

        """thing 1 is the net mask"""
        self.assertEqual( tup[1], '255.255.254.0')

        """thing 1 is the gateway"""
        self.assertEqual( tup[2], '10.228.52.1')

    #
    #Valid Linux regex
    #
    def test_linux_regex(self):
        linux_regex = if_client.os_specific['Linux']['reg']
        regex = re.compile(linux_regex)
        data = regex.findall(linux_validation_data)

        """we should capture something"""
        self.assertTrue( len(data) > 0 )
        tup = data[0]

        """we should capture 6 things actually"""
        self.assertTrue( len(tup) == 6 )

        """Cap 0 is the interface"""
        self.assertEqual( tup[0], 'eth0')

        """Cap 1 is the MAC address"""
        self.assertEqual( tup[1], '1a:15:3d:88:ed:e2')

        """Cap 2 is the upper 16bits of the IP address"""
        """Subnets may mangle the lower 16 bits"""
        """Well actually they can mangle the whole damn thing"""
        """Normally people don't mangle the whole ip address"""
        self.assertEqual( tup[2], '159.203.')

        """Now the other half the IP address"""
        self.assertEqual( tup[3], '58.254')

        """Now the subnet mask"""
        self.assertEqual( tup[4], '255.255.248.0')

        """And the default gateway"""
        self.assertEqual( tup[5], '159.203.56.1')

        """Ensure this output tuple works with linux captures function"""
        dut = if_client.linux_captures(tup)
        out = ('159.203.58.254', '255.255.248.0', '159.203.56.1')
        self.assertEqual(dut, out)

 #
 #There isn't much more I can test in a unit test fashion.
 #The rest would require a integration/os testing
 #


if __name__ == '__main__':
    unittest.main()
