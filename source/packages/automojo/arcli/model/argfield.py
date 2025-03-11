

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []

from typing import Any, Optional, TYPE_CHECKING

from automojo.arcli.model.parametertypes import ParamType, ParameterTypes


class ArgField:
    """
        A field that represents a single option in a list of options.
    """

    def __init__(self, name: str, alias: Optional[str]=None, ptype: ParamType=ParameterTypes.STRING, help: Optional[str]=None):
        """
        """
        self._name = name
        self._alias = alias
        self._ptype = ptype
        self._help = help
        return
    
    @property
    def alias(self) -> Optional[str]:
        """
            Retrieves the alias of the option field.
        """
        return self._alias

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
