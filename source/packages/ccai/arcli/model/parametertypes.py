
__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []

from ccai.arcli.model.types.paramtype import ParamType
from ccai.arcli.model.types.booltype import BoolType
from ccai.arcli.model.types.inttype import IntType
from ccai.arcli.model.types.stringtype import StringType


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
    
