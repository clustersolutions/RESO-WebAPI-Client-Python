import json
from base64 import b64encode
from urllib import parse

import requests
from bs4 import BeautifulSoup

from reso_api.exceptions import ParsingError
from reso_api.reso import RESO
from reso_api.utils import check_needed_class_vars


class OpenIDAuthentication(object):
    USERNAME_INPUTS = ['j_username', 'username', 'user', 'email']
    PASSWORD_INPUTS = ['j_password', 'password', 'pass']

    def __init__(self, reso, redirect_uri=None, scope=None, auth_code=None):
        if not isinstance(reso, RESO):
            raise ValueError('Must be of type RESO')
        self.reso = reso
        self.response_type = 'code'
        self.auth_code = auth_code
        self.scope = scope
        self.grant_type = 'authorization_code'
        self.redirect_uri = redirect_uri
        self.context = requests.Session()

    def _form_authentication_url(self, bs, return_response):
        parsed_url = parse.urlparse(self.reso.api_auth_url)
        if "{{model.loginUrl}}" in return_response['url']:
            script_tag_text = bs.find(id='modelJson').text.replace("&quot;", '"')
            script_parameters = json.loads(script_tag_text)
            self.reso.logger.info('Parsed parameters from modelJson: {}'.format(script_parameters))
            if not script_parameters.get('loginUrl'):
                raise ParsingError('Could not get loginUrl from modelJson')
            for key, value in script_parameters.items():
                if key == 'loginUrl':
                    url = parsed_url.scheme + '://' + parsed_url.netloc + script_parameters['loginUrl']
                elif key == 'antiForgery':
                    return_response['inputs'][value['name']] = value['value']
                else:
                    return_response['inputs'][key] = value
        else:
            if '://' in return_response['url']:
                url = return_response['url']
            else:
                url = parsed_url.scheme + '://' + parsed_url.netloc + return_response['url']

        self.reso.logger.debug('Formed url {}'.format(url))
        if not parse.urlparse(url):
            raise ValueError('Could not obtain RESO API login URL from the response.')
        return url

    def _fill_authentication_data(self, return_response, username, password):
        for key, value in return_response['inputs'].items():
            if value:
                continue
            if key in self.USERNAME_INPUTS:
                return_response['inputs'][key] = username
            if key in self.PASSWORD_INPUTS:
                return_response['inputs'][key] = password

    def authorize(self, username, password):
        """
        This function is dedicated for retrieving needed authorization code from OpenID server.
        :param username: username of a user
        :param password: password of a user
        :return: authorization_code
        """
        if not username or not password:
            raise ValueError('Username or password was not supplied')

        self.reso.logger.info(
            "Getting auth code for client {} (username {}) with scope {} and redirect_uri {}".format(
                self.reso.client_id, username, self.scope, self.redirect_uri
            )
        )

        # Check needed vars on OpenIDAuthentication class
        check_needed_class_vars(self, ['scope', 'redirect_uri'])
        # Check needed vars on RESO class
        check_needed_class_vars(self.reso, ['client_id', 'api_auth_url'])

        url_parameters = {
            'client_id': self.reso.client_id,
            'scope': self.scope,
            'response_type': self.response_type,
            'redirect_uri': self.redirect_uri,
        }

        # all cookies received will be stored in the session object to allow redirects form server

        self.reso.logger.info('Getting response from {} with parameters {}'.format(
            self.reso.api_auth_url, url_parameters
        ))
        response = self.context.get(self.reso.api_auth_url, params=url_parameters)

        self.reso.logger.debug('Parsing html response for form inputs')
        bs = BeautifulSoup(response.content, 'html.parser')
        raw_form = bs.find('form')
        if not raw_form:
            raise ParsingError('Could not receive authorization form. Check credentials')
        form_inputs = {
            raw_input.attrs.get('name'): raw_input.attrs.get('value') for raw_input in raw_form.find_all('input')
        }

        return_response = {
            'url': raw_form.attrs.get('action'),
            'method': raw_form.attrs.get('method'),
            'inputs': form_inputs
        }

        self.reso.logger.debug('Forming login url for posting credentials')
        url = self._form_authentication_url(bs, return_response)

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        self._fill_authentication_data(return_response, username, password)
        auth_code_response = self.context.post(url, data=return_response['inputs'], headers=headers, verify=self.reso.verify_ssl)
        self.reso.logger.info('Getting auth code from the latest redirect')
        parsed_parameters = parse.parse_qs(parse.urlparse(auth_code_response.url, allow_fragments=False).query)
        if parsed_parameters.keys():
            auth_code = parsed_parameters[list(parsed_parameters.keys())[0]]
            self.reso.logger.info('Parsed auth code from url parameters')
            return auth_code if not isinstance(auth_code, list) else auth_code[0]

        self.reso.logger.error('Could not find any parameter in url parameters.')
        raise ParsingError('Could not find any parameter in the redirect uri')

    def request_access_token(self):
        """
        Requests access token from the server provided as 'api_token_url' parameter
        :return: access_token
        """
        # Check needed vars on OpenIDAuthentication class
        check_needed_class_vars(self, ['auth_code', 'redirect_uri'])

        # Check needed vars on RESO class
        check_needed_class_vars(self.reso, ['client_id', 'client_secret', 'api_token_url'])

        auth_string = '{}:{}'.format(self.reso.client_id, self.reso.client_secret)
        headers = {
            'Authorization': 'Basic {}'.format(b64encode(auth_string.encode('utf-8')).decode('utf-8'))
        }
        url_parameters = {
            'client_id': self.reso.client_id,
            'grant_type': self.grant_type,
            'code': self.auth_code,
            'redirect_uri': self.redirect_uri,
        }
        self.reso.logger.info('Retrieving access token: {} with headers {} and parameters {}'.format(
            self.reso.api_token_url, headers, url_parameters)
        )
        access_token_response = self.context.post(self.reso.api_token_url, headers=headers, data=url_parameters)
        self.reso.logger.info('Got access_token response {}'.format(access_token_response))
        if access_token_response.status_code != 200:
            raise ValueError(access_token_response.json().get('error_description') or access_token_response.json())

        return access_token_response.json().get('access_token')

    def request_refresh_token(self):
        # TODO turned off for now this function
        return

        # Check needed vars on OpenIDAuthentication class
        check_needed_class_vars(self, ['auth_code'])

        # Check needed vars on RESO class
        check_needed_class_vars(self.reso, ['client_id', 'client_secret', 'access_token'])
        auth_string = '{}:{}'.format(self.reso.client_id, self.reso.client_secret)
        headers = {
            'Authorization': 'Basic {}'.format(b64encode(auth_string.encode('utf-8')).decode('utf-8'))
        }
        url_parameters = {
            'client_id': self.reso.client_id,
            'grant_type': 'refresh_token',
            'refresh_token': self.reso.access_token,
        }

        refresh_token_response = self.context.post(self.reso.api_token_url, headers=headers, data=url_parameters)
        self.reso.logger.info('Got response {}'.format(refresh_token_response))

        if refresh_token_response.status_code != 200:
            raise ValueError(refresh_token_response.json().get('error_description'))

        return refresh_token_response.json().get('refresh_token')

    def get_login_url(self):
        """
        Forms login url for web integrations.
        :return: formed url
        """
        # Check needed vars on OpenIDAuthentication class
        check_needed_class_vars(self, ['scope', 'redirect_uri'])

        # Check needed vars on RESO class
        check_needed_class_vars(self.reso, ['client_id', 'api_auth_url'])
        url_parameters = {
            'client_id': self.reso.client_id,
            'scope': self.scope,
            'response_type': self.response_type,
            'redirect_uri': self.redirect_uri,
        }
        return self.reso.api_auth_url + '?' + parse.urlencode(url_parameters)



