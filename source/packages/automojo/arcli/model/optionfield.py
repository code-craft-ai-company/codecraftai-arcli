
__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []

from typing import Any, Dict, Optional, TYPE_CHECKING


from automojo.errors.exceptions import SemanticError
from automojo.arcli.model.parametertypes import ParamType, ParameterTypes


if TYPE_CHECKING:
    from automojo.arcli.model.optiongroup import OptionGroup


class OptionField:
    """
        A field that represents a single option in a list of options.
    """

    def __init__(self, *flags: str, alias: Optional[str]=None, ptype: Optional[ParamType]=None, default: Optional[Any]=None,
                 required: bool=False, multiple: bool=False, count: bool=False, help: Optional[str]=None, group: Optional["OptionGroup"]=None):
        """
        """

        if alias == 'context':
            errmsg = "The word 'context' is reserved for passing the 'CliContext' object to command nodes.  It cannot be used as a parameter alias."
            raise SemanticError(errmsg)

        self._flags = flags
        self._alias = alias
        self._ptype = ptype
        self._default = default
        self._required = required
        self._multiple = multiple
        self._count = count
        self._help = help
        self._group = group


        self._flag_short = None
        self._flag_long = None
        self._flag_off = None
        
        for flag in flags:
            if flag.startswith("--"):
                if flag.find("/") > -1:
                    on_flag, off_flag = flag.split("/")
                    
                    self._flag_long = on_flag
                    self._flag_off = off_flag

                    ptype = ParameterTypes.BOOLEAN
                else:
                    self._flag_long = flag
            elif flag.startswith("-"):
                self._flag_short = flag

        # If the parameter type was not set, we need to set the parameter type to 'STRING'
        if ptype is None:
            ptype = ParameterTypes.STRING
        elif ptype == ParameterTypes.BOOLEAN and self._flag_off is None:
            self._flag_off = f"--no-{self._flag_long[2:]}"

        self._token = None
        if self._multiple:
            self._token = []
        
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
    def is_counter(self) -> bool:
        """
            Returns a value indicating if the flag is a counter flag.
        """

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
    
    def assign_alias_if_not_set(self, alias: str):
        """
            Assigns an alias to the option field if it was not already set.
        """
        if self._alias is None:
            self._alias = alias
        return

    def clone_and_fill(self, alias: str, help_fill: Dict[str, str]) -> "OptionField":
        """
            Generates a string template for the option field.
        """
        
        this_type = type(self)

        help =  self._help
        if help is not None:
            help = help.format_map(help_fill)

        clone_alias = self._alias
        if clone_alias is None:
            clone_alias= alias

        inst = this_type(self._flags, alias=clone_alias, ptype=self._ptype, default=self._default,
                         required=self._required, help=help, group=self._group)
        
        return inst


    def get_value(self) -> str:
        return self._token

    def fill_token(self, token: str):

        if self._multiple:
            self._token.append(token)
        else:
            if self._token is not None:
                errmsg = f"Duplicate token for flag {self._flag_long}."
                raise SemanticError(errmsg)

            self._token = token

        return
