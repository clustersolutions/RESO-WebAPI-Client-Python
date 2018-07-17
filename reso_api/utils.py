from reso_api.exceptions import MissingVariables


def check_needed_class_vars(self, variables):
    for var in variables:
        if not getattr(self, var):
            raise MissingVariables('Missing {} on {}'.format(var, self.__class__.__name__))
