

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []

from typing import Any, Optional, Type, TYPE_CHECKING


from automojo.errors.exceptions import SemanticError

from automojo.arcli.model.parameters.parameterbase import ParameterBase
from automojo.arcli.model.parameters.stringparameter import StringParameter

class ArgField:
    """
        A field that represents a single option in a list of options.
    """

    def __init__(self, name: str, alias: Optional[str]=None, ptype: Type[ParameterBase]=None, required: bool=True, default: Any=None, help: Optional[str]=None):
        """
        """
        if alias == 'context':
            errmsg = "The word 'context' is reserved for passing the 'CliContext' object to command nodes.  It cannot be used as a parameter alias."
            raise SemanticError(errmsg)

        if ptype is None:
            ptype = StringParameter

        self._name = name
        self._alias = alias
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
            Retrieves the alias of the option field.
        """
        return self._alias

    @property
    def default(self) -> Optional[Any]:
        return self._default

    @property
    def help(self) -> Optional[str]:
        """
            Retrieves the help of the option field.
        """
        return self._help
    
    @property
    def name(self) -> str:
        """
            Retrieves the name associated with the option field.
        """
        return self._name

    @property
    def ptype(self) -> Type[ParameterBase]:
        """
            Retrieves the name associated with the option field.
        """
        return self._ptype
    
    @property
    def required(self) -> bool:
        """
            Returns a value indicating if the argument is required.
        """
        return self._required

    def get_parameter(self) -> ParameterBase:
        param = self._ptype(self._alias, self._token)
        return param

    def fill_token(self, token: str):
        self._token = token
        return
