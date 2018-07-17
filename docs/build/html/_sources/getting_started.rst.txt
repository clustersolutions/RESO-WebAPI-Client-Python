===============
Getting started
===============

Installation
------------

The last stable release is available on PyPI and can be installed with ``pip``::

    $ pip install git+https://github.com/RESOStandards/RESO-WebAPI-Client-Python.git


Requirements
-------------

* Python:

  - Python_ >= 3.6


Dependencies
------------

The following Python extensions are required for all the RESO WebAPI Client Python SDK functions to work properly:

- BeautifulSoup_
- Urllib3_
- Requests_

Example usage
-------------

Simple usage looks like:

.. code-block:: python

    reso = RESO(
        client_id='YOUR_CLIENT_ID',
        client_secret='YOUR_CLIENT_SECRET',
        api_auth_url='https://op.api.crmls.org/identity/connect/authorize',
        api_token_url='https://op.api.crmls.org/identity/connect/token',
        api_request_url='https://h.api.crmls.org/RESO/OData/'
    )
    # Authorize user
    req_obj = OpenIDAuthentication(
            redirect_uri='https://openid.reso.org/',
            scope='ODataApi',
            reso=reso
        )
    # Get access token
    req_obj.auth_code = req_obj.authorize('USERNAME', 'PASSWORD')
    reso.access_token = req_obj.request_access_token()
    # Retrieve top 10 properties from the RESO API endpoint
    http_request = HttpRequest(reso=reso)
    result = http_request.request('Property?$top=10', 'json')
    # Display records
    print(result);

.. _Python: http://www.python.org/
.. _BeautifulSoup: https://pypi.org/project/bs4/
.. _Urllib3: https://pypi.org/project/urllib3/
.. _Requests: https://pypi.org/project/requests/