import json
import os
from unittest import TestCase
from unittest import skip

from reso_api.open_id import OpenIDAuthentication
from reso_api.request import HttpRequest
from reso_api.reso import RESO


def read_file_to_dict():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
    if os.path.isfile(file_path):
        with open(file_path) as f:
            config_dict = json.load(f)
        return config_dict
    else:
        raise ValueError('configs file is missing')


class TestIntegrationFlow(TestCase):

    @skip("This is integration test, which requires filled configs file")
    def test_flow(self):
        """
        This function tests all the flow of this SDK. To test it - remove @skip decorator
        """
        try:
            configs = read_file_to_dict()
            reso = RESO(
                client_id=configs['reso']['client_id'],
                client_secret=configs['reso']['client_secret'],
                api_auth_url=configs['reso']['api_auth_url'],
                api_token_url=configs['reso']['api_token_url'],
                verify_ssl=configs['reso']['verify_ssl'],
                api_request_url=configs['reso']['api_request_url']
            )
            reso.set_logging_level('debug')
            req_obj = OpenIDAuthentication(
                redirect_uri=configs['open_id']['redirect_uri'],
                scope=configs['open_id']['scope'],
                reso=reso
            )
            response = req_obj.authorize(configs['username'], configs['password'])
            req_obj.auth_code = response
            auth_token = req_obj.request_access_token()
            reso.access_token = auth_token
            http_req = HttpRequest(
                reso=reso,
            )
            resp = http_req.request(
                request_url=configs['http_request']['request_path'],
                request_accept_type=configs['http_request']['accept_type'],
            )
        except KeyError:
            raise ValueError('Configs file is not filled.')
        self.assertTrue(resp)
