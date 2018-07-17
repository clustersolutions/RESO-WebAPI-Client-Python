==========================================
HttpRequest (reso_api.request.HttpRequest)
==========================================


While initializing, following parameters are required:

============  ========
Parameter     Type
============  ========
reso          RESO
============  ========


Request (HttpRequest.request)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This function is dedicated for executing given url in GET method and returning full response object.

Following parameters must be set for RESO object:

* access_token
* api_request_url

This method requires these parameters:

===================  ========  ===========
Parameter            Type      Description
===================  ========  ===========
request_url          String    URL where to execute GET request
request_accept_type  String    Accept type header of a request, for example - 'application/json'
===================  ========  ===========

On successful HTTP 200 response, this function will return full response object.



Request_post (HttpRequest.request_post)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This function is dedicated for executing given url in POST method and returning full response object.

Following parameters must be set for RESO object:

* access_token
* api_request_url

This method requires these parameters:

===================  ========  ===========
Parameter            Type      Description
===================  ========  ===========
request_url          String    URL where to execute GET request
request_accept_type  String    Accept type header of a request, for example - 'application/json'
post_data            Dict      Data which must be sent
===================  ========  ===========

On successful HTTP 200 response, this function will return full response object.


Request to file (HttpRequest.request_to_file)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This function is dedicated for executing given url in GET method and returning full response content in given file.

Following parameters must be set for RESO object:

* access_token
* api_request_url

This method requires these parameters:

===================  ========  ===========
Parameter            Type      Description
===================  ========  ===========
request_url          String    URL where to execute GET request
filename             String    Full file path where to store response content
===================  ========  ===========

These parameters are optional:

===================  ========  ===========
Parameter            Type      Description
===================  ========  ===========
request_accept_type  String    Accept type header of a request, for example - 'application/json'
output_format        String    output format 'json' or 'xml', in other case. If not provided -JSON format will be user
overwrite            Boolean   Whether to overwrite file if it exists or not
===================  ========  ===========

On successful HTTP 200 response, this function will create file with full response content.



Request metadata (OpenIDAuthentication.request_metadata)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Executes metadata GET request on provided api url

Following parameters must be set for RESO object:

* access_token
* api_request_url

On successful HTTP 200 response, this function will return full response object.
