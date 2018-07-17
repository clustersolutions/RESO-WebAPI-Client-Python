from unittest import TestCase

from reso_api.request import HttpRequest
from reso_api.reso import RESO


class TestUrlsForming(TestCase):
    def test_api_request_url_endswith_backslash(self):
        backslash_url = 'http://example.com/'
        path = 'my-path'
        expected_result = backslash_url + path
        reso = RESO(api_request_url=backslash_url)
        request_obj = HttpRequest(reso)
        self.assertEquals(request_obj._return_formed_url(path), expected_result)

    def test_api_request_both_urls_have_backslashes(self):
        backslash_url = 'http://example.com/'
        path = '/my-path'
        expected_result = backslash_url[:-1] + path
        reso = RESO(api_request_url=backslash_url)
        request_obj = HttpRequest(reso)
        self.assertEquals(request_obj._return_formed_url(path), expected_result)

    def test_api_request_both_urls_without_backslashes(self):
        backslash_url = 'http://example.com'
        path = 'my-path'
        expected_result = backslash_url + '/' + path
        reso = RESO(api_request_url=backslash_url)
        request_obj = HttpRequest(reso)
        self.assertEquals(request_obj._return_formed_url(path), expected_result)

    def test_api_request_url_endswith_without_backslash(self):
        backslash_url = 'http://example.com'
        path = '/my-path'
        expected_result = backslash_url + path
        reso = RESO(api_request_url=backslash_url)
        request_obj = HttpRequest(reso)
        self.assertEquals(request_obj._return_formed_url(path), expected_result)
