
__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []

import io
import sys
from typing import Any, Callable, List, Optional, Tuple, Union, Sequence
from dataclasses import dataclass
from contextlib import redirect_stdout, redirect_stderr

@dataclass
class Result:
    """
    Holds the captured result of an invoked CLI script.
    """
    runner: "CliRunner"
    stdout: str
    stderr: str
    exit_code: int
    exception: Optional[BaseException]
    exc_info: Optional[Tuple[type, BaseException, Any]] = None

    @property
    def output(self) -> str:
        """The (standard) output as unicode string."""
        return self.stdout

class CliRunner:
    """
    The CLI runner provides functionality to invoke a command-line script for testing purposes.
    """

    def __init__(self, charset: str = "utf-8"):
        self.charset = charset

    def invoke(
        self,
        cli: Callable,
        args: Optional[Union[str, Sequence[str]]] = None,
        prog_name: Optional[str] = None,
        catch_exceptions: bool = True,
        **extra: Any,
    ) -> Result:
        """
        Invokes a command in an isolated environment.

        :param cli: The command object or callable to invoke.
        :param args: The arguments to invoke the command with.
        :param prog_name: The program name to use.
        :param catch_exceptions: Whether to catch exceptions (other than SystemExit).
        :return: A Result object.
        """
        if args is None:
            args = []
        elif isinstance(args, str):
             # Split string args if provided as a single string (naive splitting)
            import shlex
            args = shlex.split(args)

        stdout = io.StringIO()
        stderr = io.StringIO()

        exit_code = 0
        exception = None
        exc_info = None

        try:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                # We need to simulate how EntryCommand is called.
                # If cli is an EntryCommand instance, it has a __call__ method.
                # It accepts prog_name and args (which should be the list of arguments excluding the program name if called directly with args)

                # However, EntryCommand.__call__ takes `args` which are typically sys.argv[1:].
                # So we pass `args` directly.

                # Check if it accepts the arguments we want to pass
                # For now, assuming it's an EntryCommand or compatible callable

                # Note: EntryCommand.__call__ signature: (self, *, prog_name: Optional[str] = None, args: Optional[Sequence[str]] = None) -> int

                # We try to pass as keyword arguments if it seems to be our EntryCommand,
                # but if it's a raw function it might expect something else.
                # Let's assume standard behavior for now: invoke it.

                # If it's an arcli EntryCommand, it returns an int (exit code).
                result = cli(prog_name=prog_name, args=args)
                if isinstance(result, int):
                    exit_code = result

        except SystemExit as e:
            exit_code = e.code if e.code is not None else 0
            if exit_code != 0:
                exception = e
                exc_info = sys.exc_info()
        except Exception as e:
            exception = e
            exc_info = sys.exc_info()
            if not catch_exceptions:
                raise
            exit_code = 1

        return Result(
            runner=self,
            stdout=stdout.getvalue(),
            stderr=stderr.getvalue(),
            exit_code=exit_code,
            exception=exception,
            exc_info=exc_info,
        )
