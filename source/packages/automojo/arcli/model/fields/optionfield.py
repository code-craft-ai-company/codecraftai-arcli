
__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []

from typing import Any, Dict, Optional, Type, TYPE_CHECKING


from enum import IntEnum


from automojo.errors.exceptions import SemanticError, MissingOptionError
from automojo.arcli.model.parameters.parameterbase import ParameterBase
from automojo.arcli.model.parameters.defaultparameter import DefaultParameter

from automojo.arcli.model.parameters.booleanparameter import BooleanParameter
from automojo.arcli.model.parameters.integerparameter import IntegerParameter
from automojo.arcli.model.parameters.stringparameter import StringParameter
from automojo.arcli.model.parameters.listofstringparameter import ListOfStringParameter


if TYPE_CHECKING:
    from automojo.arcli.model.optiongroup import OptionGroup


class OptionMode(IntEnum):
    """
        Enumeration defining the different modes of operation for option fields.
        
        OptionMode specifies how an option field should behave when processing
        command-line arguments, determining whether it accepts single values,
        multiple values, or acts as a counter.
    """
    Simple = 0
    Multiple = 1
    Counter = 2


class OptionField:
    """
        Field representing a command-line option parameter.
        
        OptionField defines a flag-based option that can be passed to a command-line interface.
        Options are identified by flags (short like -v or long like --verbose) and can
        operate in different modes: simple (single value), multiple (list of values),
        or counter (count occurrences).
        
        This class manages the configuration, validation, and parsing of option parameters
        including their flags, types, default values, help text, and operational modes.
    """

    def __init__(self, *flags: str, alias: Optional[str]=None, ptype: Type[ParameterBase]=None, default: Optional[Any]=None,
                 required: bool=False, mode: OptionMode=OptionMode.Simple, help: Optional[str]=None, group: Optional["OptionGroup"]=None):
        """
            Initialize a new OptionField instance.
            
            Creates an option field with the specified flags and configuration. Automatically
            determines parameter types based on flags and mode, and validates that reserved
            names are not used as aliases.
            
            :param flags: Variable number of flag strings (e.g., '-v', '--verbose')
            :param alias: Optional alias for the option parameter
            :param ptype: Parameter type class for value parsing and validation
            :param default: Default value for the option
            :param required: Whether the option is required
            :param mode: Operation mode for the option (Simple, Multiple, Counter)
            :param help: Help text describing the option
            :param group: Optional option group this option belongs to
            
            :raises: SemanticError
        """

        if alias == 'context':
            errmsg = "The word 'context' is reserved for passing the 'CliContext' object to command nodes.  It cannot be used as a parameter alias."
            raise SemanticError(errmsg)

        self._flags = flags
        self._alias = alias
        self._default = default
        self._required = required
        self._mode = mode
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

                    ptype = BooleanParameter
                else:
                    self._flag_long = flag
            elif flag.startswith("-"):
                self._flag_short = flag

        # If the parameter type was not set, we need to set the parameter type to 'STRING'
        if ptype is None:
            if self._mode == OptionMode.Counter:
                ptype = IntegerParameter
            elif self._mode == OptionMode.Multiple:
                ptype = ListOfStringParameter
            else:
                ptype = StringParameter

        elif ptype == BooleanParameter and self._flag_off is None:
            self._flag_off = f"--no-{self._flag_long[2:]}"

        self._ptype = ptype

        self._token = None
        if self._mode == OptionMode.Multiple or self._mode == OptionMode.Counter:
            self._token = []
        
        return
    
    @property
    def alias(self) -> Optional[str]:
        """
            Get the alias of the option field.
            
            :returns: The alias name used for parameter mapping, or None if not set
        """
        return self._alias
    
    @property
    def default(self) -> Optional[Any]:
        """
            Get the default value for this option field.
            
            :returns: The default value for the option, or None if not set
        """
        return self._default
    
    @property
    def flag_long(self) -> Optional[str]:
        """
            Get the long flag for this option field.
            
            :returns: The long flag string (e.g., '--verbose'), or None if not set
        """
        return self._flag_long

    @property
    def flag_short(self) -> Optional[str]:
        """
            Get the short flag for this option field.
            
            :returns: The short flag string (e.g., '-v'), or None if not set
        """
        return self._flag_short

    @property
    def help(self) -> Optional[str]:
        """
            Get the help text for this option field.
            
            :returns: The help text describing the option, or None if not provided
        """
        return self._help

    @property
    def mode(self) -> OptionMode:
        """
            Get the operation mode for this option field.
            
            :returns: The OptionMode indicating how the option processes values
        """
        return self._mode

    @property
    def ptype(self) -> Type[ParameterBase]:
        """
            Get the parameter type class for this option field.
            
            :returns: The parameter type class used for parsing and validation
        """
        return self._ptype

    @property
    def required(self) -> bool:
        """
            Check if this option is required.
            
            :returns: True if the option is required, False if optional
        """
        return self._required
    
    def assign_alias_if_not_set(self, alias: str):
        """
            Assign an alias to the option field if it was not already set.
            
            This method is used to set the alias for an option field when it's being
            processed from an option group or when the alias needs to be determined
            automatically from context.
            
            :param alias: The alias name to assign if none is currently set
        """
        if self._alias is None:
            self._alias = alias
        return

    def clone_and_fill(self, alias: str, help_fill: Dict[str, str]) -> "OptionField":
        """
            Create a clone of this option field with template substitution.
            
            Generates a new OptionField instance with the same configuration as this one,
            but with help text template variables filled in and optionally a new alias.
            This is useful for creating customized versions of option fields.
            
            :param alias: The alias to use for the cloned field
            :param help_fill: Dictionary of template variables to substitute in help text
            
            :returns: A new OptionField instance with filled templates
        """
        
        this_type = type(self)

        help =  self._help
        if help is not None:
            help = help.format_map(help_fill)

        clone_alias = self._alias
        if clone_alias is None:
            clone_alias= alias

        inst = this_type(*self._flags, alias=clone_alias, ptype=self._ptype, default=self._default,
                         required=self._required, mode=self._mode, help=help, group=self._group)
        
        return inst


    def get_parameter(self) -> ParameterBase:
        """
            Create a parameter instance from this option field.
            
            Instantiates the parameter type class with the field's alias and processed
            token value. Handles different option modes (counter, multiple, simple)
            and applies default values or raises errors for missing required options.
            
            :returns: A parameter instance configured with this field's settings
            
            :raises: MissingOptionError
        """
        
        tvalue = self._token
        token_missing = tvalue is None

        if not token_missing and self._mode in (OptionMode.Counter, OptionMode.Multiple):
            token_missing = len(self._token) == 0

        if token_missing and self._default is not None:
            param = DefaultParameter(self._alias, self._default)
            return param

        if tvalue is not None:
            if self._mode == OptionMode.Counter:
                tvalue = len(self._token)

        else:
            if self._required:
                errmsg = f"The '{self._flags}' option is required but was not provided."
                option_name = self._flag_long or self._flag_short or str(self._flags)
                option_type = self._ptype.__name__ if self._ptype else "unknown"
                hint = f"Please provide the {option_name} option."
                raise MissingOptionError(errmsg, option_name, option_type, hint)

        param = self._ptype(self._alias, tvalue)
        
        return param


    def fill_token(self, token: str):
        """
            Set or append a token value for this option field.
            
            Stores the raw command-line token that will be processed by the parameter type.
            Handles different option modes: simple options store a single value, while
            multiple and counter modes accumulate values in a list.
            
            :param token: The raw command-line token value
            
            :raises: SemanticError
        """

        if token is not None:

            if self._mode == OptionMode.Counter or self._mode == OptionMode.Multiple:
                self._token.append(token)
            else:
                if self._token is not None:
                    errmsg = f"Duplicate token for flag {self._flag_long}."
                    raise SemanticError(errmsg)

                self._token = token

        return
