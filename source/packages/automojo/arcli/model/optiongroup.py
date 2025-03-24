
__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []

from typing import Dict, Optional, TYPE_CHECKING

from automojo.errors.exceptions import SemanticError

from automojo.arcli.model.optionfield import OptionField

if TYPE_CHECKING:
    from automojo.arcli.model.command import Command

class OptionGroup:

    name: str = ""

    def __init__(self):
        self.name = self.name.strip()

        if self.name == "":
            this_type = type(self)
            class_name = this_type.__name__
            errmsg = f"Option groups must be named.  Did you set the 'name' class attribute on the class='{class_name}'"
            raise SemanticError(errmsg)

        return

    @classmethod
    def attach(cls, help_fill: Optional[Dict[str, str]]=None):

        def decorator(command: Command):

            if not isinstance(command, Command):
                errmsg = "The innermost decorator for a command must be 'entry', 'group' or 'command'"
                raise SemanticError(errmsg)
            
            command.add_option_group(cls)

            return command

        return decorator





