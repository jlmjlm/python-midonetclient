# Copyright 2012 Midokura Japan KK

import os
import sys
import unittest
from webob import exc

TOPDIR = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]),
                                   os.pardir,
                                   os.pardir,
                                   os.pardir))
sys.path.insert(0, TOPDIR)

from midonet.client import MidonetClient
from midonet import utils


class TestBridge(unittest.TestCase):

    tenent = None
    bridge = None
    bridge_uuid = None
    test_tenant_name = "TEST_TENANT"
    test_bridge_name = "TEST_BRIDGE"

    @classmethod
    def setUpClass(cls):
        mc = MidonetClient()
        cls.tenant = mc.tenants()
        cls.bridge = mc.bridges()
        cls.dhcp = mc.dhcps()
        cls.dhcp_host = mc.dhcp_hosts()

        try:
            cls.tenant.create(cls.test_tenant_name)
            r, c = cls.bridge.create(cls.test_tenant_name, cls.test_bridge_name)
            cls.bridge_uuid = utils.get_uuid(r)
            r, c = cls.dhcp.create(cls.test_tenant_name, cls.bridge_uuid,
                                '172.16.0.0', 16, '172.16.0.1')
        except:
            pass

    @classmethod
    def tearDownClass(cls):
        cls.tenant.delete(cls.test_tenant_name)


    def test_create_get_delete(self):
        r, c = self.dhcp_host.create(self.test_tenant_name, self.bridge_uuid,
                                     '172.16.0.0_16', '00:00:00:11:11:11', '172.16.1.100',
                                     'test-name')


        r, c = self.dhcp_host.list(self.test_tenant_name, self.bridge_uuid, '172.16.0.0_16')

        self.dhcp_host.get(self.test_tenant_name, self.bridge_uuid, '172.16.0.0_16', '00:00:00:11:11:11')
        self.dhcp_host.delete(self.test_tenant_name, self.bridge_uuid, '172.16.0.0_16', '00:00:00:11:11:11')

        #TODO: Fix mgmt to return 404. Currently server return 500
        #self.assertRaises(exc.HTTPNotFound, self.dhcp.get, self.test_tenant_name, self.bridge_uuid, '172.16.0.0_16')
if __name__ == '__main__':
    unittest.main()
