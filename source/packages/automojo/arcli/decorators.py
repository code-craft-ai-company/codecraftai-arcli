

from typing import Any, Optional

import collections

from automojo.arcli.model.argfield import ArgField
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


def option(name: str, alias: Optional[str]=None, ptype: ParamType=ParameterTypes.STRING, default: Optional[Any]=None,
           required: bool=False, help: Optional[str]=None, group: Optional[str]=None):
    """
        A decorator that creates an option field.
    """

    def decorator(func):
        """
            The decorator function.
        """
        field = OptionField(name, alias, ptype, default, required, help, group)

        if not hasattr(func, "__flags_long__"):
            func.__flags_long__ = {}

        if not hasattr(func, "__flags_short__"):
            func.__flags_short__ = {}

        if not hasattr(func, "__req_options__"):
            func.__req_options__ = []
        
        if not hasattr(func, "__opt_options__"):
            func.__opt_options__ = []
        
        if field.flag_short in func.__flags_short__:
            raise ValueError(f"Duplicate short flag: {field.flag_short}")
        
        if field.flag_long in func.__flags_long__:
            raise ValueError(f"Duplicate long flag: {field.flag_long}")

        if field.required:
            func.__req_options__.append(field)
        else:
            func.__opt_options__.append(field)

        return func

    return decorator
