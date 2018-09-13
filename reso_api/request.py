import json
import os
import xml.etree.cElementTree as ElementTree
from urllib import parse

import requests

from reso_api.constants import FORMATS
from reso_api.exceptions import RequestError, ParsingError
from reso_api.reso import RESO
from reso_api.utils import check_needed_class_vars


class HttpRequest(object):

    def __init__(self, reso):
        if not isinstance(reso, RESO):
            raise ValueError('Must be of type RESO')

        self.reso = reso

    def _return_formed_url(self, request_url):
        typical_case = self.reso.api_request_url + request_url
        if self.reso.api_request_url.endswith('/'):
            if not request_url.startswith('/'):
                returnable_url = typical_case
            else:
                returnable_url = self.reso.api_request_url[:-1] + request_url
        else:
            if not request_url.startswith('/'):
                returnable_url = self.reso.api_request_url + '/' + request_url
            else:
                returnable_url = typical_case

        if not parse.urlparse(returnable_url):
            raise ValueError('Could not parse request url: {}'.format(returnable_url))
        return returnable_url

    @staticmethod
    def _form_request_accept_type(accept_type):
        formed_accept_type = accept_type
        if formed_accept_type:
            if '/' not in accept_type:
                formed_accept_type = 'application/' + accept_type
        else:
            formed_accept_type = '*/*'
        return formed_accept_type

    @staticmethod
    def _validate_path(overwrite, filename):
        full_file_path = filename
        if not os.path.dirname(filename):
            raise ValueError('Need full path. Provided path - {}'.format(full_file_path))
        if os.path.isfile(full_file_path) and not overwrite:
            raise ValueError('File already exists at {}. '
                             'Set "overwrite" to True if you want to overwrite the file'.format(full_file_path)
                             )

        if not os.path.exists(os.path.dirname(full_file_path)):
            raise ValueError('Directory does not exist at {}'.format(full_file_path))

        return full_file_path

    def request(self, request_url, request_accept_type):
        """
        Executes GET request on specified request_url
        :param request_url: path where to execute GET request
        :param request_accept_type: request accept type header value
        :return: returns response object on successful HTTP 200 request
        """
        # Check needed vars on RESO class
        check_needed_class_vars(self.reso, ['api_request_url', 'access_token'])

        self.reso.logger.debug('Forming request url')
        formed_request_url = self._return_formed_url(request_url)

        request_accept_type = self._form_request_accept_type(request_accept_type)
        headers = {
            'Accept': request_accept_type,
            'Authorization': 'Bearer ' + self.reso.access_token
        }

        self.reso.logger.debug('Sending GET request to {}'.format(formed_request_url))
        response = requests.get(formed_request_url, headers=headers, verify=self.reso.verify_ssl)
        self.reso.logger.info('Got GET {} response {}'.format(formed_request_url, response))
        if not response or response.status_code != 200:
            if response.status_code == 406:
                raise RequestError(
                    "API returned HTTP code 406 - Not Acceptable. "
                    "Please, setup a valid request accept type, current - {}".format(request_accept_type)
                )
            else:
                try:
                    msg = response.json()
                except json.decoder.JSONDecodeError:
                    msg = response
                raise RequestError(
                    "Could not retrieve API response. "
                    "Response: {}".format(msg)
                )
        return response

    def request_post(self, request_url, request_accept_type, post_data):
        """
        Executes POST request on specified request_url
        :param request_url: path where to execute POST request
        :param request_accept_type: request accept type header value
        :param post_data: data which should be sent via POST request
        :return: returns response object on successful HTTP 200 request
        """
        if not isinstance(post_data, dict):
            raise ParsingError('\'post_data\' must be of instance dict')
        # Check needed vars on RESO class
        check_needed_class_vars(self.reso, ['api_request_url', 'access_token'])

        self.reso.logger.debug('Forming request url')
        formed_request_url = self._return_formed_url(request_url)

        request_accept_type = self._form_request_accept_type(request_accept_type)

        headers = {
            'Accept': request_accept_type,
            'Authorization': 'Bearer ' + self.reso.access_token
        }

        self.reso.logger.debug('Sending POST request to {}'.format(formed_request_url))
        response = requests.post(formed_request_url, headers=headers, data=post_data, verify=self.reso.verify_ssl)
        self.reso.logger.info('Got POST {} response {}'.format(formed_request_url, response))
        if not response or response.status_code != 200:
            if response.status_code == 406:
                raise RequestError(
                    "API returned HTTP code 406 - Not Acceptable. "
                    "Please, setup a valid request accept type, current - {}".format(request_accept_type)
                )
            else:
                raise RequestError(
                    "Could not retrieve API response. "
                    "Response: {}".format(response.json() if response.json() else response)
                )
        return response

    def request_to_file(self, request_url, filename, request_accept_type=None,
                        output_format=None, overwrite=False, indent=None):
        """
        Executes GET request and stores received content in a file.
        :param request_url: path where to execute GET request
        :param filename: full path of file where to store response info
        :param request_accept_type: request accept type header value
        :param output_format: output format 'json' or 'xml'
        :param overwrite: whether overwrite file in case it exists or not
        :param indent: Pretty format json output with tab space <indent>. None is no indent
        :return: True in case function has been completed successfully
        """
        full_file_path = self._validate_path(overwrite, filename)

        if not output_format or output_format.lower() not in FORMATS.VALID_OUTPUT_FORMATS:
            output_format = FORMATS.JSON_FORMAT

        if output_format.lower() == FORMATS.XML_FORMAT:
            request_accept_type = 'xml'
        elif output_format.lower() == FORMATS.JSON_FORMAT:
            request_accept_type = 'json'

        response = self.request(request_url, request_accept_type)

        self.reso.logger.info('Writing to file')
        # Opening file for bytes writing because of xml format
        with open(full_file_path, 'w+b') as f:
            try:
                if output_format == FORMATS.JSON_FORMAT:
                    f.write(json.dumps(response.json(), indent=indent).encode('utf-8'))
                elif output_format == FORMATS.XML_FORMAT:
                    root = ElementTree.fromstring(response.text)
                    tree = ElementTree.ElementTree(root)
                    tree.write(f)
                else:
                    raise ValueError('No defined formatter for {}'.format(output_format))
            except Exception as e:
                self.reso.logger.info('Writing without format because of: {}'.format(e))
                f.write(response.content)

        return True

    def request_metadata(self):
        """
        Executes metadata GET request on provided api url
        :return: response of received metadata
        """
        self.reso.logger.info('Requesting resource metadata')
        return self.request('$metadata', request_accept_type=None)
