import logging

from reso_api import API_LOGGER_NAME, LOGGER_MAP


class RESO(object):

    def __init__(self, client_id=None, client_secret=None, access_token=None, api_auth_url=None, api_token_url=None,
                 api_request_url=None, verify_ssl=False):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.api_auth_url = api_auth_url
        self.api_token_url = api_token_url
        self.api_request_url = api_request_url
        self.verify_ssl = verify_ssl
        self.api_sdk_version = '0.0.2'

        self.logger = logging.getLogger(API_LOGGER_NAME)
        self.logger.setLevel(logging.WARNING)

        stream = logging.StreamHandler()
        stream.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        stream.setLevel(logging.DEBUG)

        self.logger.addHandler(stream)

    def disable_logger(self):
        self.logger.disabled = True

    def enable_logger(self):
        self.logger.disabled = False

    def set_logging_level(self, level):
        if str(level).lower() not in LOGGER_MAP.keys():
            raise ValueError('Incorrect logging level. Possible values: {}'.format(LOGGER_MAP.keys()))

        self.logger.setLevel(LOGGER_MAP[level.lower()])
