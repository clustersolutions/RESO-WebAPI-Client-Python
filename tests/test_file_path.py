import os
from unittest import TestCase

from reso_api.request import HttpRequest
from reso_api.reso import RESO


class TestPathValidation(TestCase):

    def setUp(self):
        reso = RESO()
        self.request_obj = HttpRequest(reso)
        self.filename = 'example.json'

    def test_validate_relative_path(self):
        with self.assertRaises(ValueError) as context:
            self.request_obj._validate_path('test_url', self.filename)

        self.assertEquals('Need full path. Provided path - {}'.format(self.filename), str(context.exception))

    def test_valid_full_path(self):
        path = os.path.join(os.path.abspath(__file__), self.filename)
        returned_path = self.request_obj._validate_path('test_url', path)
        self.assertEquals(returned_path, path)

    def test_dir_does_not_exist(self):
        path = os.path.join(os.path.join(os.path.abspath(__file__), 'dir-which-does-not-exist'), self.filename)
        with self.assertRaises(ValueError) as context:
            self.request_obj._validate_path('test_url', path)

        self.assertEquals('Directory does not exist at {}'.format(path), str(context.exception))
