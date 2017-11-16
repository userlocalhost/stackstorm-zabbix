import mock

from zabbix_base_action_test_case import ZabbixBaseActionTestCase
from host_delete import HostDelete

from urllib2 import URLError
from pyzabbix.api import ZabbixAPIException


class HostDeleteTestCase(ZabbixBaseActionTestCase):
    __test__ = True
    action_cls = HostDelete

    @mock.patch('lib.actions.ZabbixBaseAction.find_host')
    @mock.patch('lib.actions.ZabbixBaseAction.connect')
    def test_run_connection_error(self, mock_connect, mock_find_host):
        action = self.get_action_instance(self.full_config)
        mock_connect.side_effect = URLError('connection error')
        test_dict = {'host': "test"}
        host_dict = {'name': "test", 'hostid': '1'}
        mock_find_host.return_vaue = host_dict

        with self.assertRaises(URLError):
            action.run(**test_dict)

    @mock.patch('lib.actions.ZabbixBaseAction.find_host')
    @mock.patch('lib.actions.ZabbixBaseAction.connect')
    def test_run_host_error(self, mock_connect, mock_find_host):
        action = self.get_action_instance(self.full_config)
        mock_connect.return_vaue = "connect return"
        test_dict = {'host': "test"}
        host_dict = {'name': "test", 'hostid': '1'}
        mock_find_host.side_effect = ZabbixAPIException('host error')
        mock_find_host.return_vaue = host_dict
        action.connect = mock_connect
        action.find_host = mock_find_host

        with self.assertRaises(ZabbixAPIException):
            action.run(**test_dict)

    @mock.patch('lib.actions.ZabbixAPI')
    @mock.patch('lib.actions.ZabbixBaseAction.connect')
    def test_run(self, mock_connect, mock_client):
        action = self.get_action_instance(self.full_config)
        mock_connect.return_vaue = "connect return"
        test_dict = {'host': "test"}
        host_dict = {'name': "test", 'hostid': '1'}
        action.connect = mock_connect
        action.find_host = mock.MagicMock(return_value=host_dict)
        mock_client.host.delete.return_value = "delete return"
        action.client = mock_client

        result = action.run(**test_dict)
        mock_client.host.delete.assert_called_with(host_dict['hostid'])
        self.assertEqual(result, True)

    @mock.patch('lib.actions.ZabbixAPI')
    @mock.patch('lib.actions.ZabbixBaseAction.connect')
    def test_run_delete_error(self, mock_connect, mock_client):
        action = self.get_action_instance(self.full_config)
        mock_connect.return_vaue = "connect return"
        test_dict = {'host': "test"}
        host_dict = {'name': "test", 'hostid': '1'}
        action.connect = mock_connect
        action.find_host = mock.MagicMock(return_value=host_dict)
        mock_client.host.delete.side_effect = ZabbixAPIException('host error')
        mock_client.host.delete.return_value = "delete return"
        action.client = mock_client

        with self.assertRaises(ZabbixAPIException):
            action.run(**test_dict)
