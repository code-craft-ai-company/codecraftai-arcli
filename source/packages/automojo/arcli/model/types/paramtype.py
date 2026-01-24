
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
