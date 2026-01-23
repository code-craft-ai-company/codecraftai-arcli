__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []

from typing import Any, Optional

import sys
import threading
import time
import itertools
from enum import Enum

class InteractionStrategy(str, Enum):
    NEVER = "never"
    ALLOW = "allow"

def prompt_for_input(prompt_text: str, default: Optional[str] = None, required: bool = True) -> str:
    """
    Prompts the user for input.
    """
    prompt_str = f"{prompt_text}"
    if default is not None:
        prompt_str += f" [{default}]"
    prompt_str += ": "

    while True:
        val = input(prompt_str).strip()
        if not val:
            if default is not None:
                return default
            if required:
                print("Error: This field is required.")
                continue
            return "" # Not required, empty string
        return val

def confirm(prompt_text: str, default: bool = False) -> bool:
    """
    Prompts the user for confirmation (y/N).
    """
    yes_opts = ['y', 'yes']
    no_opts = ['n', 'no']

    if default:
        prompt_str = f"{prompt_text} [Y/n]: "
    else:
        prompt_str = f"{prompt_text} [y/N]: "

    while True:
        val = input(prompt_str).strip().lower()
        if not val:
            return default

        if val in yes_opts:
            return True
        elif val in no_opts:
            return False

        print("Please enter 'y' or 'n'.")

class Spinner:
    """
    A simple spinner for terminal output.
    """
    def __init__(self, message: str = "Processing... ", delay: float = 0.1):
        self.spinner = itertools.cycle(['|', '/', '-', '\\'])
        self.delay = delay
        self.busy = False
        self.spinner_visible = False
        self.message = message

    def write_next(self):
        sys.stdout.write(next(self.spinner))
        sys.stdout.flush()
        sys.stdout.write('\b')
        sys.stdout.flush()

    def _spinner_task(self):
        sys.stdout.write(self.message)
        sys.stdout.flush()
        while self.busy:
            self.write_next()
            time.sleep(self.delay)

        # Clear line
        sys.stdout.write('\r')
        sys.stdout.flush()
        sys.stdout.write(' ' * (len(self.message) + 1))
        sys.stdout.write('\r')
        sys.stdout.flush()

    def __enter__(self):
        if sys.stdout.isatty():
            self.busy = True
            self._thread = threading.Thread(target=self._spinner_task)
            self._thread.start()
        return self

    def __exit__(self, exception, value, tb):
        if self.busy:
            self.busy = False
            if hasattr(self, '_thread'):
                self._thread.join()

        if exception is not None:
            return False
