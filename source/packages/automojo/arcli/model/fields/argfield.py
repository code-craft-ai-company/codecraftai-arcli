

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []

from typing import Any, Optional, Type, TYPE_CHECKING


from automojo.errors.exceptions import SemanticError

from automojo.arcli.model.parameters.parameterbase import ParameterBase
from automojo.arcli.model.parameters.defaultparameter import DefaultParameter
from automojo.arcli.model.parameters.stringparameter import StringParameter

class ArgField:
    """
        Field representing a command-line argument parameter.
        
        ArgField defines a positional argument that can be passed to a command-line interface.
        Unlike options, arguments are positional and typically required. This class manages
        the configuration, validation, and parsing of argument parameters including their
        names, types, default values, and help text.
        
        Arguments are processed in order and can be either required or optional with default
        values. The field handles type conversion and validation through parameter types.
    """

    def __init__(self, name: str, alias: Optional[str]=None, ptype: Type[ParameterBase]=None, required: bool=True, default: Any=None, help: Optional[str]=None):
        """
            Initialize a new ArgField instance.
            
            Creates an argument field with the specified configuration. Validates that
            optional arguments have default values and that reserved names are not used.
            
            :param name: The name of the argument field
            :param alias: Optional alias for the argument parameter
            :param ptype: Parameter type class for value parsing and validation
            :param required: Whether the argument is required
            :param default: Default value for optional arguments
            :param help: Help text describing the argument
            
            :raises: SemanticError
        """
        if alias == 'context':
            errmsg = "The word 'context' is reserved for passing the 'CliContext' object to command nodes.  It cannot be used as a parameter alias."
            raise SemanticError(errmsg)

        if ptype is None:
            ptype = StringParameter

        self._name = name
        self._alias = alias if alias is not None else name
        self._ptype = ptype
        self._required = required
        self._default = default
        self._help = help

        if not self._required and self._default is None:
            errmsg = "Optional argument fields must have a default value."
            raise SemanticError(errmsg)

        self._token = None
        return

    @property
    def alias(self) -> Optional[str]:
        """
            Get the alias of the argument field.
            
            :returns: The alias name used for parameter mapping, or None if not set
        """
        return self._alias

    @property
    def default(self) -> Optional[Any]:
        """
            Get the default value for this argument field.
            
            :returns: The default value for optional arguments, or None for required arguments
        """
        return self._default

    @property
    def help(self) -> Optional[str]:
        """
            Get the help text for this argument field.
            
            :returns: The help text describing the argument, or None if not provided
        """
        return self._help
    
    @property
    def name(self) -> str:
        """
            Get the name of this argument field.
            
            :returns: The name associated with the argument field
        """
        return self._name

    @property
    def ptype(self) -> Type[ParameterBase]:
        """
            Get the parameter type class for this argument field.
            
            :returns: The parameter type class used for parsing and validation
        """
        return self._ptype
    
    @property
    def required(self) -> bool:
        """
            Check if this argument is required.
            
            :returns: True if the argument is required, False if optional
        """
        return self._required

    def get_parameter(self) -> ParameterBase:
        """
            Create a parameter instance from this argument field.
            
            Instantiates the parameter type class with the field's alias and token value
            to create a parameter object that can be used for value parsing and retrieval.
            
            :returns: A parameter instance configured with this field's settings
        """
        if self._token is None and self._default is not None:
            param = DefaultParameter(self._alias, self._default)
        else:
            param = self._ptype(self._alias, self._token)
        return param

    def fill_token(self, token: str):
        """
            Set the token value for this argument field.
            
            Stores the raw command-line token that will be parsed by the parameter type
            when get_parameter() is called. This method is used during argument parsing
            to associate command-line values with argument fields.
            
            :param token: The raw command-line token value
        """
        self._token = token
        return
