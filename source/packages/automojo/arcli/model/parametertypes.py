
__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []

from automojo.arcli.model.types.paramtype import ParamType
from automojo.arcli.model.types.booltype import BoolType
from automojo.arcli.model.types.inttype import IntType
from automojo.arcli.model.types.stringtype import StringType


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
    
