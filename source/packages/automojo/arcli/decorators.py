

from typing import Any, Optional

import collections

from automojo.errors.exceptions import SemanticError

from automojo.arcli.model.argfield import ArgField
from automojo.arcli.model.command import Command
from automojo.arcli.model.entrycommand import EntryCommand
from automojo.arcli.model.groupingcommand import GroupingCommand
from automojo.arcli.model.optionfield import OptionField
from automojo.arcli.model.parametertypes import ParamType, ParameterTypes  


def argument(name: str, alias: Optional[str]=None, ptype: ParamType=ParameterTypes.STRING, help: Optional[str]=None):
    """
        A decorator that creates an argument field.
    """

    def decorator(func):
        """
            The decorator function.
        """

        field = ArgField(name, alias, ptype, help)
        
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

        return

    return decorator

def entry(name: Optional[str]=None):
    
    def decorator(func):
        nonlocal name

        if name is None:
            func_name: str = func.__name__
            name = func_name.replace("_", "-")

        cmdobj = EntryCommand(name, func)

        return cmdobj

    return decorator

def group(name: Optional[str]=None):
    
    def decorator(func):
        nonlocal name

        if name is None:
            func_name: str = func.__name__
            name = func_name.replace("_", "-")

            cmdobj = GroupingCommand(name, func)

        return

    return decorator


def option(*flags: str, alias: Optional[str]=None, ptype: ParamType=ParameterTypes.STRING, default: Optional[Any]=None,
           required: bool=False, help: Optional[str]=None, group: Optional[str]=None):
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

        opt_field = OptionField(*flags, alias=assign_alias, ptype=ptype, default=default, required=required, help=help, group=group)

        command.add_option(opt_field)

        return command

    return decorator


