
__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []

from typing import Any, Dict, Optional, TYPE_CHECKING

from automojo.arcli.model.parametertypes import ParamType, ParameterTypes


if TYPE_CHECKING:
    from automojo.arcli.model.optiongroup import OptionGroup


class OptionField:
    """
        A field that represents a single option in a list of options.
    """

    def __init__(self, *flags: str, name: str, alias: Optional[str]=None, ptype: ParamType=ParameterTypes.STRING, default: Optional[Any]=None,
                 required: bool=False, help: Optional[str]=None, group: Optional["OptionGroup"]=None):
        """
        """

        self._flags = flags

        self._flag_short = None
        self._flag_long = None
        for flag in flags:
            if flag.startswith("--"):
                self._flag_long = flag
            elif flag.startswith("-"):
                self._flag_short = flag

        if self._flag_short is None and self._flag_long is None:
            raise ValueError("At least one flag, single-dash or double-dash, must be provided.")

        self._name = name
        self._alias = alias
        self._ptype = ptype
        self._default = default
        self._required = required
        self._help = help
        self._group = group
        return
    
    @property
    def alias(self) -> Optional[str]:
        """
            Retrieves the alias of the option field.
        """
        return self._alias
    
    @property
    def default(self) -> Optional[Any]:
        """
            Retrieves the default value of the option field.
        """
        return self._default
    
    @property
    def flag_long(self) -> Optional[str]:
        """
            Retrieves the flag_short of the option field.
        """
        return self._flag_long

    @property
    def flag_short(self) -> Optional[str]:
        """
            Retrieves the flag_short of the option field.
        """
        return self._flag_short

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
            Retrieves the required status of the option field.
        """
        return self._required

    def assign_alias(self, alias: str):
        """
            Assigns an alias to the option field.
        """
        self._alias = alias
        return
    
    def assign_alias_if_not_set(self, alias: str):
        """
            Assigns an alias to the option field if it was not already set.
        """
        if self._alias is None:
            self._alias = alias
        return

    def instantiate(self, help_fill: Dict[str, str]) -> "OptionField":
        """
            Generates a string template for the option field.
        """
        
        this_type = type(self)

        help =  self._help
        if help is not None:
            help = help.format_map(help_fill)

        inst = this_type(self._flags, self._name, self._alias, self._ptype, self._default, self._required, help, self._group)
        
        return inst
