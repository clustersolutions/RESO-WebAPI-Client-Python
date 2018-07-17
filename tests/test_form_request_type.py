from unittest import TestCase

from reso_api.request import HttpRequest
from reso_api.reso import RESO


class TestRequestTypeForming(TestCase):

    def setUp(self):
        reso = RESO()
        self.request_obj = HttpRequest(reso)

    def test_accept_type_simple_case(self):
        accept_type = 'json'
        expected_result = 'application/json'
        self.assertEquals(self.request_obj._form_request_accept_type(accept_type), expected_result)

    def test_no_accept_type(self):
        accept_type = None
        expected_result = '*/*'
        self.assertEquals(self.request_obj._form_request_accept_type(accept_type), expected_result)

    def test_full_accept_type(self):
        accept_type = 'application/xml'
        expected_result = 'application/xml'
        self.assertEquals(self.request_obj._form_request_accept_type(accept_type), expected_result)
