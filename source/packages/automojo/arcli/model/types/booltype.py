
__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []

from automojo.arcli.model.types.paramtype import ParamType

class BoolType(ParamType):
    """
        Parameter type representing boolean values.

        BoolType is used to define command-line parameters that accept boolean values
        such as flags or true/false options. This type is typically used for options
        that can be either present or absent, or that accept explicit true/false values.
    """

    name: str = "boolean"
