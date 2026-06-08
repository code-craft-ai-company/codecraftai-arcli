
__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []

from typing import Any, Callable, Dict, Optional, TYPE_CHECKING

from ccai.errors.exceptions import SemanticError

if TYPE_CHECKING:
    from ccai.arcli.model.optiongroup import OptionGroup


class TrapField:
    """
        Field representing a command-line trap option that triggers immediate action.
        
        TrapField defines a special type of option that performs an action and halts
        command execution when encountered. Trap options are high-priority flags that
        execute a callback function immediately during parsing, typically used for
        help displays, version information, or other utility functions.
        
        Unlike regular options, trap fields do not pass values to the main command
        callback but instead execute their own callback and terminate processing.
    """

    def __init__(self, *flags: str, trap_callback: Callable, help: Optional[str]=None, group: Optional["OptionGroup"]=None):
        """
            Initialize a new TrapField instance.
            
            Creates a trap field with the specified flags and callback function.
            The callback will be executed immediately when the trap flag is encountered
            during command-line parsing.
            
            :param flags: Variable number of flag strings (e.g., '-h', '--help')
            :param trap_callback: Function to call when the trap is triggered
            :param help: Help text describing the trap option
            :param group: Optional option group this trap belongs to
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
            Get the long flag for this trap field.
            
            :returns: The long flag string (e.g., '--help'), or None if not set
        """
        return self._flag_long

    @property
    def flag_short(self) -> Optional[str]:
        """
            Get the short flag for this trap field.
            
            :returns: The short flag string (e.g., '-h'), or None if not set
        """
        return self._flag_short

    @property
    def help(self) -> Optional[str]:
        """
            Get the help text for this trap field.
            
            :returns: The help text describing the trap option, or None if not provided
        """
        return self._help

    def call_trap_callback(self):
        """
            Execute the trap callback function.
            
            Invokes the callback function associated with this trap field. This method
            is called during command-line parsing when the trap flag is encountered,
            allowing the trap to perform its action and halt further processing.
        """
        self._trap_callback()
        return
