

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from typing import Callable, Sequence, Optional


import sys
import inspect

from automojo.errors.exceptions import SemanticError

from automojo.arcli.model.clicontext import CliContext
from automojo.arcli.model.groupingcommand import GroupingCommand
from automojo.arcli.model.fields.trapfield import TrapField

from automojo.arcli.parsing import ProgressiveOptionParser
from automojo.arcli.interact import InteractionStrategy


def detect_program_name() -> str:
    """
        Detect the program name from command line arguments.
        
        :returns: The program name from sys.argv[0]
    """
    arg0 = sys.argv[0]
    return arg0


class EntryCommand(GroupingCommand):
    """
        Entry point command for command-line interface applications.
        
        EntryCommand extends GroupingCommand to serve as the root command for CLI applications.
        It handles the initial parsing of command-line arguments and provides the entry point
        for command execution. This class manages the program name, CLI context, and coordinates
        the overall command execution flow.
        
        The EntryCommand can be called directly to process command-line arguments and execute
        the appropriate command hierarchy based on the parsed input.
    """

    def __init__(self, name: str, callable: Callable, prog_name: Optional[str] = None, version: Optional[str] = None,
                 interaction_strategy: InteractionStrategy = InteractionStrategy.NEVER):
        """
            Initialize a new EntryCommand instance.
            
            :param name: The name of the entry command
            :param callable: The function to be called when this command is executed
            :param prog_name: Optional program name, auto-detected if not provided
            :param version: Optional version string
            :param interaction_strategy: The interaction strategy to use
        """
        super().__init__(name, callable)

        if prog_name is None:
            prog_name = detect_program_name()

        self._prog_name = prog_name
        self._version = version

        self._context = CliContext(interaction_strategy=interaction_strategy)

        if self._version:
            self.add_trap(TrapField("--version", trap_callback=self._version_callback, help="Show the version and exit."))

        return

    def _version_callback(self):
        print(self._version)
        exit(0)

    @property
    def program_name(self) -> str:
        """
            Get the program name for this entry command.
            
            :returns: The program name used for this CLI application
        """
        return self._prog_name

    def _command_entry(self, prog_name: str, args: Sequence[str]) -> int:
        """
            Add an option group to this command.
            
            This method processes all OptionField objects in the option group class
            and registers them with this command.
            
            :param option_group: The option group class containing OptionField objects
        """
        # Create a full argv list with program name + args for the parser
        full_argv = [prog_name] + list(args)
        parser = ProgressiveOptionParser(full_argv)

        self.prepare_callargs(self._context, parser)
        self.call_command()

        return 0  # Success

    def __call__(self, *,  prog_name: Optional[str] = None, args: Optional[Sequence[str]] = None) -> int:
        """
            Execute the entry command with the provided or default arguments.
            
            This method serves as the main entry point for CLI execution. It can be called
            directly to process command-line arguments and execute the appropriate command
            hierarchy. If no arguments are provided, it uses sys.argv by default.
            
            :param prog_name: Optional program name, auto-detected if not provided
            :param args: Optional command-line arguments, uses sys.argv[1:] if not provided
            
            :returns: The result of command execution
        """

        if prog_name is None:
            prog_name = detect_program_name()

        if args is None:
            args = sys.argv[1:]
            
        return self._command_entry(prog_name, args)