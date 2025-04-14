
from typing import Callable, Sequence, Optional


import sys
import inspect

from automojo.errors.exceptions import SemanticError

from automojo.arcli.model.clicontext import CliContext
from automojo.arcli.model.groupingcommand import GroupingCommand

from automojo.arcli.parsing import ProgressiveOptionParser


def detect_program_name() -> str:
    arg0 = sys.argv[0]
    return arg0


class EntryCommand(GroupingCommand):

    def __init__(self, name: str, callable: Callable, prog_name: Optional[str] = None):
        super().__init__(name, callable)

        if prog_name is None:
            prog_name = detect_program_name()

        self._prog_name = prog_name

        self._context = CliContext()

        return

    @property
    def program_name(self) -> str:
        return self._prog_name

    def _command_entry(self, prog_name: str, args: Sequence[str]):

        parser = ProgressiveOptionParser(sys.argv)

        self.prepare_callargs(self._context, parser)

        self.call_command()

        return

    def __call__(self, *,  prog_name: Optional[str] = None, args: Optional[Sequence[str]] = None):

        if prog_name is None:
            prog_name = detect_program_name()

        if args is None:
            args = sys.argv[1:]
            
        rtnval = self._command_entry(prog_name, args)

        return rtnval