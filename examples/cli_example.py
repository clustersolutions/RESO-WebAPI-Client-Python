#!/usr/bin/env python

import os
import json

from reso_api.reso import RESO
from reso_api.open_id import OpenIDAuthentication
from reso_api.request import HttpRequest


def read_file_to_dict():

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
    if os.path.isfile(file_path):
        with open(file_path) as f:
            config_dict = json.load(f)
        return config_dict
    else:
        raise ValueError('configs file is missing')


def cli_example():
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
    http_req.request_to_file(
        request_url=configs['http_request']['request_path'],
        filename=configs['http_request']['filename'],
        request_accept_type=configs['http_request']['accept_type'],
        output_format=configs['http_request']['output_format']
    )


if __name__ == '__main__':
    cli_example()
