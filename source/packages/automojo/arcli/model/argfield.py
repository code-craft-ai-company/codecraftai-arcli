

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []

from typing import Any, Optional, TYPE_CHECKING


from automojo.errors.exceptions import SemanticError
from automojo.arcli.model.parametertypes import ParamType, ParameterTypes


class ArgField:
    """
        A field that represents a single option in a list of options.
    """

    def __init__(self, name: str, alias: Optional[str]=None, ptype: ParamType=ParameterTypes.STRING, required: bool=True, default: Any=None, help: Optional[str]=None):
        """
        """
        if alias == 'context':
            errmsg = "The word 'context' is reserved for passing the 'CliContext' object to command nodes.  It cannot be used as a parameter alias."
            raise SemanticError(errmsg)

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
    def ptype(self) -> ParamType:
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

    def get_value(self) -> str:
        return self._token

    def fill_token(self, token: str):
        self._token = token
        return
