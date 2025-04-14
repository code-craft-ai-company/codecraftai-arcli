
__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []

class ParamType:
    """
    """

    name: str

class BoolType(ParamType):
    """
    A parameter type that represents a boolean.
    """

    name: str = "boolean"

class IntType(ParamType):
    """
    A parameter type that represents a integer.
    """

    name: str = "integer"

class StringType(ParamType):
    """
    A parameter type that represents a string.
    """

    name: str = "string"



class ParameterTypes:

    BOOLEAN = BoolType
    INT = IntType
    STRING = StringType
    

