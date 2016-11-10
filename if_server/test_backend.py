import datetime
import unittest
import backend
import sqlite3

class TestObject(unittest.TestCase):

    #
    #Validate date regex
    #
    def test_backend_date_regex(self):
        
        """declare test strings"""
        dut0 = "2011-11-05"     #pass
        dut1 = " 2011-11-05"    #fail
        dut2 = "2011-11-05 "    #fail
        dut3 = "2011-11-5"      #fail

        """local var"""
        re = backend.validate_date

        """run tests"""
        self.assertTrue(re.match(dut0))
        self.assertFalse(re.match(dut1))
        self.assertFalse(re.match(dut2))
        self.assertFalse(re.match(dut3))
       
    #
    #Validate ip regex
    #
    def test_backend_ip_regex(self):

        """declare test strings"""
        dut0 = "255.255.255.0"  #pass
        dut1 = "192.168.0.1"    #pass
        dut2 = " 255.255.61.8"  #fail
        dut3 = "1.2.3.4"        #pass
        dut4 = "999.999.999.999"#pass
        dut5 = "6.3.2.1 "       #fail

        """localized regex"""
        re = backend.validate_ip

        """run tests"""
        self.assertTrue(re.match(dut0))
        self.assertTrue(re.match(dut1))
        self.assertFalse(re.match(dut2))
        self.assertTrue(re.match(dut3))
        self.assertTrue(re.match(dut4))
        self.assertFalse(re.match(dut5))

    #
    #Validate number regex
    #
    def test_backend_num_regex(self):
        
        """declare test strings"""
        dut0 = "0"              #pass
        dut1 = "a"              #fail
        dut2 = " 1"             #fail
        dut3 = "1 "             #fail
        dut4 = "2000"           #pass

        """localize regex"""
        re = backend.validate_num

        """run tests"""
        self.assertTrue(re.match(dut0))
        self.assertFalse(re.match(dut1))
        self.assertFalse(re.match(dut2))
        self.assertFalse(re.match(dut3))
        self.assertTrue(re.match(dut4))


    #
    #Validate the Insert query function
    #
    def test_backend_make_insert_query(self):

        """declare vars"""
        host = "WLaeder"
        today = "2016-11-10"
        iface = "0"
        ipv4 = "10.228.63.151"
        mask = "255.255.248.0"
        gate = "10.228.0.1"

        """collect result"""
        (err,query) = backend.make_insert_query(host,today,iface,ipv4,mask,gate)

        """insepct"""
        self.assertEqual(err,0)
        self.assertEqual(query, "INSERT INTO address VALUES ('WLaeder','2016-11-10',0,'10.228.63.151','255.255.248.0','10.228.0.1');")



if __name__ == '__main__':
    unittest.main()
