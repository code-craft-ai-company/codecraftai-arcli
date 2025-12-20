

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []

from typing import Callable

import inspect

from automojo.errors.exceptions import SemanticError
from automojo.arcli.model.command import Command

from automojo.arcli.model.clicontext import CliContext
from automojo.arcli.parsing import ProgressiveOptionParser

class GroupingCommand(Command):
    """
        A command that can contain and manage child commands, creating a hierarchical command structure.
        
        GroupingCommand extends the base Command class to support nested command structures where
        a parent command can have multiple child commands. This enables the creation of command-line
        interfaces with subcommands, similar to tools like git or docker.
        
        The GroupingCommand maintains a collection of child commands and handles the delegation
        of execution to the appropriate child command based on the command-line arguments.
    """

    def __init__(self, name: str, callable: Callable):
        """
            Initialize a new GroupingCommand instance.
            
            :param name: The name of the grouping command
            :param callable: The function to be called when this command is executed
        """
        super().__init__(name, callable)

        self._command_nodes = {}

        self._callchild = None
        return

    @property
    def has_children(self) -> bool:
        """
            Check if this grouping command has any child commands.
            
            :returns: True if the command has one or more child commands, False otherwise
        """
        rtnval = len(self._command_nodes) > 0
        return rtnval

    def add_command(self, command: Command):
        """
            Add a child command to this grouping command.
            
            This method registers a child command that can be invoked as a subcommand
            of this grouping command. The child command will be accessible by its name
            when parsing command-line arguments.
            
            :param command: The command object to add as a child command
            :raises: SemanticError
        """

        if not isinstance(command, Command):
            errmsg = "You must provide a decorated 'Command' method."
            raise SemanticError(errmsg)

        cmdname = command.name
        self._command_nodes[cmdname] = command

        return

    def has_child_command(self, cmdname: str):
        """
            Check if a child command with the specified name exists.
            
            This method determines whether a child command with the given name
            has been registered with this grouping command.
            
            :param cmdname: The name of the child command to check for
            :returns: True if a child command with the specified name exists, False otherwise
        """
        
        exists = False
        if cmdname in self._command_nodes:
            exists = True

        return exists

    def call_command(self):
        """
            Execute this grouping command and optionally delegate to a child command.
            
            This method first executes the callable associated with this grouping command
            using the prepared call arguments. If a child command has been designated for
            execution (_callchild is set), it will then delegate execution to that child
            command by calling its call_command method.
            
            The execution flow allows for both the parent grouping command and a child
            command to be executed in sequence, enabling complex command hierarchies
            where parent commands can perform setup or validation before child execution.
        """

        self._callable(*self._callargs)

        if self._callchild is not None:
            child_command = self._command_nodes[self._callchild]
            child_command.call_command()

        return

    def prepare_callargs(self, context: CliContext, parser: ProgressiveOptionParser):
        # First prepare this command's arguments
        super().prepare_callargs(context, parser)
        
        # Check if there's a child command to process
        if self.has_children and parser._index_cursor < len(parser._arg_components):
            next_component = parser._arg_components[parser._index_cursor]
            if self.has_child_command(next_component):
                self._callchild = next_component
                parser._index_cursor += 1  # Move past the child command name
                
                # Prepare the child command's arguments
                child_command = self._command_nodes[self._callchild]
                child_command.prepare_callargs(context, parser)
        
        return
