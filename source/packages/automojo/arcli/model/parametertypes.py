
__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []

class ParamType:
    """
        Base class for parameter type definitions.
        
        ParamType serves as the foundation for all parameter type classes in the CLI framework.
        It defines the basic structure that all parameter types must follow, including the
        requirement for a name attribute that identifies the parameter type.
        
        This class is intended to be subclassed by specific parameter type implementations
        such as BoolType, IntType, and StringType.
    """

    name: str

class BoolType(ParamType):
    """
        Parameter type representing boolean values.
        
        BoolType is used to define command-line parameters that accept boolean values
        such as flags or true/false options. This type is typically used for options
        that can be either present or absent, or that accept explicit true/false values.
    """

    name: str = "boolean"

class IntType(ParamType):
    """
        Parameter type representing integer values.
        
        IntType is used to define command-line parameters that accept integer numeric values.
        This type handles the parsing and validation of integer inputs from command-line
        arguments, ensuring that only valid integer values are accepted.
    """

    name: str = "integer"

class StringType(ParamType):
    """
        Parameter type representing string values.
        
        StringType is used to define command-line parameters that accept text string values.
        This is the most common parameter type and handles the parsing of string inputs
        from command-line arguments, preserving the text content as provided by the user.
    """

    name: str = "string"



class ParameterTypes:
    """
        Registry class providing access to all available parameter types.
        
        ParameterTypes serves as a centralized registry and factory for parameter type
        classes used throughout the CLI framework. It provides convenient class-level
        constants for accessing the standard parameter types without needing to import
        each type individually.
        
        This class acts as a namespace for parameter type constants, making it easy
        to reference parameter types consistently across the codebase.
    """

    BOOLEAN = BoolType
    INT = IntType
    STRING = StringType
    

