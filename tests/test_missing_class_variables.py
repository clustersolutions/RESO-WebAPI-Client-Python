from unittest import TestCase

from reso_api.exceptions import MissingVariables
from reso_api.reso import RESO
from reso_api.utils import check_needed_class_vars


class TestMissingClassVariables(TestCase):

    def test_validate_missing_variable(self):
        reso = RESO()
        variable = 'client_id'
        with self.assertRaises(MissingVariables) as context:
            check_needed_class_vars(reso, [variable])

        self.assertEquals('Missing {} on {}'.format(variable, reso.__class__.__name__), str(context.exception))

    def test_validate_no_missing_variable(self):
        reso = RESO(client_id='some-client-id')
        variable = 'client_id'
        check_needed_class_vars(reso, [variable])
