
__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []

from typing import Dict, Optional, TYPE_CHECKING

from ccai.errors.exceptions import SemanticError

from ccai.arcli.model.fields.optionfield import OptionField

if TYPE_CHECKING:
    from ccai.arcli.model.command import Command

class OptionGroup:
    """
        Base class for grouping related command-line options together.
        
        OptionGroup provides a way to organize related command-line options into logical
        groups for better organization and help display. Option groups must have a name
        and can be attached to commands using the attach decorator method.
        
        This class serves as a container for OptionField objects and provides validation
        to ensure that option groups are properly named before use.
    """

    name: str = ""

    def __init__(self):
        """
            Initialize a new OptionGroup instance.
            
            Validates that the option group has a non-empty name set as a class attribute.
            
            :raises: SemanticError
        """
        self.name = self.name.strip()

        if self.name == "":
            this_type = type(self)
            class_name = this_type.__name__
            errmsg = f"Option groups must be named.  Did you set the 'name' class attribute on the class='{class_name}'"
            raise SemanticError(errmsg)

        return

    @classmethod
    def attach(cls, help_fill: Optional[Dict[str, str]]=None):
        """
            Decorator method to attach this option group to a command.
            
            This class method returns a decorator that can be applied to Command objects
            to register all options in this option group with the command. It provides
            a convenient way to add multiple related options to a command at once.
            
            :param help_fill: Optional dictionary for help text customization
            
            :returns: Decorator function that attaches the option group to a command
        """

        def decorator(command: "Command"):
            from ccai.arcli.model.command import Command

            if not isinstance(command, Command):
                errmsg = "The innermost decorator for a command must be 'entry', 'group' or 'command'"
                raise SemanticError(errmsg)
            
            command.add_option_group(cls, help_fill)

            return command

        return decorator





