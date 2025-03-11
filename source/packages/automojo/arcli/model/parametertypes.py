
__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []

class ParamType:
    """
    """

    name: str


class IntType(ParamType):
    """
    A parameter type that represents a string.
    """

    name: str = "integer"

class StringType(ParamType):
    """
    A parameter type that represents a string.
    """

    name: str = "string"



class ParameterTypes:

    INT = IntType
    STRING = StringType

