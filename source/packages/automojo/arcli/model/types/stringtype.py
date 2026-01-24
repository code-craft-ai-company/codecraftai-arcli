
__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []

from automojo.arcli.model.types.paramtype import ParamType

class StringType(ParamType):
    """
        Parameter type representing string values.

        StringType is used to define command-line parameters that accept text string values.
        This is the most common parameter type and handles the parsing of string inputs
        from command-line arguments, preserving the text content as provided by the user.
    """

    name: str = "string"
