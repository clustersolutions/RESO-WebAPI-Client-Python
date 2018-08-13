# RESO SDK Python

This is a client library to interface with a RESO certified Web API server. For more information on the Real Estate Standards Organization (RESO) please visit [www.reso.org](http://www.reso.org) or contact [github@reso.org](mailto:github@reso.org). Developers wishing to better understand how to use and contribute to our standards visit [RESO Developers FAQ](https://www.reso.org/developer-faqs/working-with-github/).

Specific questions about this repository should be posted to the 'Issues' section with the [Issue Template](ISSUE_TEMPLATE.md). 

All documentation can be found in -[`docs`](https://github.com/RESOStandards/RESO-WebAPI-Client-Python/blob/master/docs/build/html/index.html) folder.

## Requirements

Python 3.6 and later.

## PIP

Install package via pip:
```
pip install git+https://github.com/RESOStandards/RESO-WebAPI-Client-Python.git
```

## Dependencies

The following Python extensions are required for all the RESO WebAPI Client Python SDK functions to work properly:

- [`bs4`](https://pypi.org/project/bs4/)
- [`urllib3`](https://pypi.org/project/urllib3/)
- [`requests`](https://pypi.org/project/requests/)


## Getting Started

Simple usage looks like:

```Python
# Set the variables
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
```

## Example apps

Several usage examples are provided in the [`examples/`](https://github.com/RESOStandards/RESO-WebAPI-Client-Python/tree/master/examples) folder:

- [`cli-example`](https://github.com/RESOStandards/RESO-WebAPI-Client-Python/blob/master/examples/cli_example.py) - provides a sample console application to query RESO API data;

To configure the example app variables / settings - fill config.json file.

## Configuring a Logger

The SDK has a built-in logger for debug / testing purposes. Usage:

```python
# Set logging. Logger is enabled by default
reso.disable_logger() # disables logger
reso.enable_logger() # enables logger
reso.set_logging_level('debug') # sets logging level. Possible values: 'debug', 'info', 'warning'

```

## Unit Tests

The SDK code set contains Python unit tests. The tests reside in the [`tests/`](https://github.com/RESOStandards/RESO-WebAPI-Client-Python/tree/master/tests) folder and covers core RESO WebAPI Client Python SDK functionality testing.

To run the tests fill the tests/config.json file with the appropriate API variables. Then, execute:

```
python setup.py test
```

## Contributing

Please read the [contributing guidelines](CONTRIBUTING.md) if You are interested in contributing to the project.
