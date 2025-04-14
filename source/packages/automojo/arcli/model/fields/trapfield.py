
__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []

from typing import Any, Callable, Dict, Optional, TYPE_CHECKING


from automojo.errors.exceptions import SemanticError
from automojo.arcli.model.parametertypes import ParamType, ParameterTypes


if TYPE_CHECKING:
    from automojo.arcli.model.optiongroup import OptionGroup


class TrapField:
    """
        A field that represents a single option in a list of options that acts as a trap.
    """

    def __init__(self, *flags: str, trap_callback: Callable, help: Optional[str]=None, group: Optional["OptionGroup"]=None):
        """
        """

        self._flags = flags
        self._trap_callback = trap_callback
        self._help = help
        self._group = group

        self._flag_short = None
        self._flag_long = None

        for flag in flags:
            if flag.startswith("--"):
                self._flag_long = flag
            elif flag.startswith("-"):
                self._flag_short = flag

        return
    
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

    def call_trap_callback(self):
        """
            Calls the trap callback associated with a given 'trap' option.
        """
        self._trap_callback()
        return
