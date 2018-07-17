============================================================
OpenIDAuthentication (reso_api.open_id.OpenIDAuthentication)
============================================================


While initializing, following parameters are required:

============  ========
Parameter     Type
============  ========
reso          RESO
============  ========

While initializing, following parameters are optional:

============  ========
Parameter     Type
============  ========
auth_code     String
scope         String
redirect_uri  String
============  ========


Authorize (OpenIDAuthentication.authorize)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This function is dedicated for retrieving needed authorization code from OpenID server.

Following parameters must be set for OpenIDAuthentication object:

* scope
* redirect_uri

Following parameters must be set for RESO object:

* client_id
* api_auth_url

This method requires these parameters:

============  ========  ===========
Parameter     Type      Description
============  ========  ===========
username      String    Username or email of a user
password      String    Password of a user
============  ========  ===========

On successful case, this function will return authorization code, which must be used for retrieving access token.



Request access token (OpenIDAuthentication.request_access_token)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Requests access token from the server provided as 'api_token_url' parameter.

Following parameters must be set for OpenIDAuthentication object:

* auth_code
* redirect_uri

Following parameters must be set for RESO object:

* client_id
* client_secret
* api_token_url

On successful request access token will be returned



Get login url (OpenIDAuthentication.get_login_url)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Forms login url for web integrations.

Following parameters must be set for OpenIDAuthentication object:

* scope
* redirect_uri

Following parameters must be set for RESO object:

* client_id
* api_auth_url

On successful call - full url will be returned with formed url parameters
