__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []

from automojo.errors.exceptions import SemanticError

class MissingOptionError(SemanticError):
    def __init__(self, message, option_name, option_type, hint):
        super().__init__(message)
        self.option_name = option_name
        self.option_type = option_type
        self.hint = hint
