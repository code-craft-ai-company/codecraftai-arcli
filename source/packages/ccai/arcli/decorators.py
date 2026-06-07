

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []

from typing import Any, Callable, Optional, Type

import collections

from ccai.errors.exceptions import SemanticError


from ccai.arcli.model.command import Command
from ccai.arcli.model.entrycommand import EntryCommand
from ccai.arcli.model.groupingcommand import GroupingCommand
from ccai.arcli.model.fields.argfield import ArgField
from ccai.arcli.model.fields.optionfield import OptionField, OptionMode
from ccai.arcli.model.fields.trapfield import TrapField
from ccai.arcli.model.parameters.parameterbase import ParameterBase
from ccai.arcli.interact import InteractionStrategy


def argument(name: str, alias: Optional[str]=None, ptype: Type[ParameterBase]=None, required: bool=True, default: Any=None, help: Optional[str]=None):
    """
        A decorator that creates an argument field.
    """

    def decorator(func):
        """
            The decorator function.
        """

        field = ArgField(name, alias, ptype, required, default, help)
        
        if isinstance(func, Command):
            func.add_argument(field)
            return func

        if not hasattr(func, "__arguments__"):
            func.__arguments__ = collections.OrderedDict()
        
        if name in func.__arguments__:
            errmsg = f"Duplicate argument name '{name}'"
            raise ValueError(errmsg)
        
        func.__arguments__[name] = field

        return func

    return decorator

def command(name: Optional[str]=None):
    
    def decorator(func):
        nonlocal name

        if name is None:
            func_name: str = func.__name__
            name = func_name.replace("_", "-")

        cmdobj = Command(name, func)
        return cmdobj

    return decorator

def entry(name: Optional[str]=None, version: Optional[str]=None, interaction_strategy: InteractionStrategy=InteractionStrategy.NEVER):
    
    def decorator(func):
        nonlocal name

        if name is None:
            func_name: str = func.__name__
            name = func_name.replace("_", "-")

        cmdobj = EntryCommand(name, func, version=version, interaction_strategy=interaction_strategy)

        return cmdobj

    return decorator

def group(name: Optional[str]=None):
    
    def decorator(func):
        nonlocal name

        if name is None:
            func_name: str = func.__name__
            name = func_name.replace("_", "-")

        cmdobj = GroupingCommand(name, func)
        return cmdobj

    return decorator


def option(*flags: str, alias: Optional[str]=None, ptype: Type[ParameterBase]=None, default: Optional[Any]=None,
           required: bool=False, mode: OptionMode=OptionMode.Simple, help: Optional[str]=None, group: Optional[str]=None):
    """
        A decorator that creates an option field.
    """

    def decorator(command):
        """
            The decorator function.
        """

        if not isinstance(command, Command):
            errmsg = "The innermost decorator for a command must be 'entry', 'group' or 'command'"
            raise SemanticError(errmsg)

        if len(flags) == 0:
            errmsg = "Each option must have a flag."
            raise SemanticError(errmsg)

        if len(flags) > 2:
            errmsg = "Each option can have only one double dash '--' flag and one single dash '-' flag."
            raise SemanticError(errmsg)
        
        flag_long = None

        if len(flags) == 1:
            if not flags[0].startswith("--"):
                errmsg = "Each option must have have a '--' flag."
                raise SemanticError(errmsg)
            flag_long = flags[0]
        else:
            double_dash_count = 0
            single_dash_count = 0
        
            # Verify flags
            for flag in flags:
                if flag.startswith("--"):
                    double_dash_count += 1
                    flag_long = flag
                elif flag.startswith("-"):
                    single_dash_count += 1

            if double_dash_count > 1:
                errmsg = "An option is only allowed to have one double dash '--' flag."
                raise SemanticError(errmsg)
            
            if single_dash_count > 1:
                errmsg = "An option is only allowed to have one single dash '-' flag."
                raise SemanticError(errmsg)

        assign_alias = flag_long.lstrip("-").replace("-", "_")
        if alias is not None:
            assign_alias = alias

        opt_field = OptionField(*flags, alias=assign_alias, ptype=ptype, default=default, required=required, mode=mode, help=help, group=group)

        command.add_option(opt_field)

        return command

    return decorator


def trap(*flags: str, trap_callback: Callable, help: Optional[str]=None, group: Optional[str]=None):
    """
        A decorator that creates an trap optional field.
    """

    def decorator(command):
        """
            The decorator function.
        """

        if not isinstance(command, Command):
            errmsg = "The innermost decorator for a command must be 'entry', 'group' or 'command'"
            raise SemanticError(errmsg)

        if len(flags) == 0:
            errmsg = "Each trap must have a flag."
            raise SemanticError(errmsg)

        if len(flags) > 2:
            errmsg = "Each option can have only one double dash '--' flag and one single dash '-' flag."
            raise SemanticError(errmsg)

        if len(flags) == 1:
            if not flags[0].startswith("--"):
                errmsg = "Each option must have have a '--' flag."
                raise SemanticError(errmsg)
        else:
            double_dash_count = 0
            single_dash_count = 0
        
            # Verify flags
            for flag in flags:
                if flag.startswith("--"):
                    double_dash_count += 1
                elif flag.startswith("-"):
                    single_dash_count += 1

            if double_dash_count > 1:
                errmsg = "An trap is only allowed to have one double dash '--' flag."
                raise SemanticError(errmsg)
            
            if single_dash_count > 1:
                errmsg = "An trap is only allowed to have one single dash '-' flag."
                raise SemanticError(errmsg)

        trap_field = TrapField(*flags, trap_callback=trap_callback, help=help, group=group)

        command.add_trap(trap_field)

        return command

    return decorator

