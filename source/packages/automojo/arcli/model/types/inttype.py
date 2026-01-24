
__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []

from automojo.arcli.model.types.paramtype import ParamType

class IntType(ParamType):
    """
        Parameter type representing integer values.

        IntType is used to define command-line parameters that accept integer numeric values.
        This type handles the parsing and validation of integer inputs from command-line
        arguments, ensuring that only valid integer values are accepted.
    """

    name: str = "integer"
