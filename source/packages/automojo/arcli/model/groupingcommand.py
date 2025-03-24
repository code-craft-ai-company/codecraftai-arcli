
from typing import Callable

from automojo.arcli.model.command import Command

class GroupingCommand(Command):

    def __init__(self, name: str, callable: Callable):
        super().__init__(name, callable)
        return