
from typing import Callable

import inspect

from automojo.errors.exceptions import SemanticError
from automojo.arcli.model.command import Command

from automojo.arcli.model.clicontext import CliContext
from automojo.arcli.parsing import ProgressiveOptionParser

class GroupingCommand(Command):

    def __init__(self, name: str, callable: Callable):
        super().__init__(name, callable)

        self._command_nodes = {}

        self._callchild = None
        return
    
    @property
    def has_children(self) -> bool:
        rtnval = len(self._command_nodes) > 0
        return rtnval

    def add_command(self, command: Command):

        if not isinstance(command, Command):
            errmsg = "You must provide a decorated 'Command' method."
            raise SemanticError(errmsg)

        cmdname = command.name
        self._command_nodes[cmdname] = command

        return
    
    def has_child_command(self, cmdname: str):
        
        exists = False
        if cmdname in self._command_nodes:
            exists = True

        return exists

    def prepare_callargs(self, context: CliContext, parser: ProgressiveOptionParser):

        callargs = []

        sigspec = inspect.signature(self._callable)

        argnames = [aname for aname in sigspec.parameters.keys()]
        if argnames[0] == 'context':
            callargs.append(context)

        parameter_table = parser.parse_parameters_for_command(self)

        for argn in argnames:
            if argn in parameter_table:
                param = parameter_table[argn]
                argv = param.get_value()
                callargs.append(argv)
            else:
                fname = self._callable.__name__
                errmsg = f"The {argn} parameter for function '{fname}' could not be found."
                raise SemanticError(errmsg)

        return
    
    def call_command(self):

        self._callable(*self._callargs)

        if self._callchild is not None:
            child_command = self._command_nodes[self._callchild]
            child_command.call_command()

        return