=========================
RESO (reso_api.reso.RESO)
=========================

While initializing, following parameters are optional:

===============  ========
Parameter        Type
===============  ========
client_id        String
client_secret    String
access_token     String
api_auth_url     String
api_token_url    String
api_request_url  String
verify_ssl       Boolean
===============  ========


Disable logger (RESO.disable_logger)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This function is dedicated for disabling API logger (Enabled by default).


Enable logger (RESO.enable_logger)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This function is dedicated for enabling API logger.


Set logging level (RESO.set_logging_level)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This function is dedicated for changing logging level of API logger (Defaul is 'info').

This method requires this parameter:

============  ========  ===========
Parameter     Type      Description
============  ========  ===========
level         String    Possible values: 'debug', 'info', 'warning'
============  ========  ===========
