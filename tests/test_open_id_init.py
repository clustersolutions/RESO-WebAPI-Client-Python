from unittest import TestCase

from reso_api.open_id import OpenIDAuthentication


class TestOpenID(TestCase):

    def test_failing_open_id_init(self):
        with self.assertRaises(ValueError) as context:
            OpenIDAuthentication(reso='reso')

        self.assertEquals('Must be of type RESO', str(context.exception))
