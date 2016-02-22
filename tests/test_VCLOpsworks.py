"""Tests for VCL Opsworks."""

import unittest
import getpass
import VCLOpsworks.config

#from nose.tools import ok_, eq_, raises
#from nose import SkipTest

class VclopsworksTestCase(unittest.TestCase):
    def setUp(self):
        config = config.Config()
        url = "https://vcl.ncsu.edu/scheduling/index.php?mode=xmlrpccall"
        username = "agoel3@NCSU"
        password = getpass.getpass()
        VCLOpsworks.make_config(config, url, username, password)

    def tearDown(self):
        pass

    def test_VCLOpsworks(self):
        # do something to test VCLOpsworks
        pass
