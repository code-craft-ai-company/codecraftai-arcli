
from typing import Callable, Sequence, Optional, Union

from automojo.arcli.model.command import Command

import sys



def detect_program_name() -> str:
    arg0 = sys.argv[0]
    return arg0


class EntryCommand(Command):

    def __init__(self, name: str, callable: Callable, prog_name: Optional[str] = None):
        super().__init__(name, callable)

        if prog_name is None:
            prog_name = detect_program_name()

        self._prog_name = prog_name

        return
    
    @property
    def program_name(self) -> str:
        return self._prog_name

    def _command_entry(self, prog_name: str, args: Sequence[str]):

        
        return

    def __call__(self, *,  prog_name: Optional[str] = None, args: Optional[Sequence[str]] = None):

        if prog_name is None:
            prog_name = detect_program_name()

        if args is None:
            args = sys.argv[1:]
            
        return self._command_entry(prog_name, args)