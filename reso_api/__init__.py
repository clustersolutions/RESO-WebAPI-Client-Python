import urllib3

# disabling SSL cert warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import logging

# It must appear here for a proper name retrieval
API_LOGGER_NAME = __name__
LOGGER_MAP = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}
