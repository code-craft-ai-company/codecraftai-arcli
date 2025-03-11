
__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []

from typing import Dict, Optional


from automojo.arcli.model.optionfield import OptionField


class OptionGroup:

    name: str

    def __init__(self):
        self.name = self.name
        return

    @classmethod
    def attach(cls, help_fill: Optional[Dict[str, str]]=None):

        def decorator(func):

            if not hasattr(func, "__flags_long__"):
                func.__flags_long__ = {}

            if not hasattr(func, "__flags_short__"):
                func.__flags_short__ = {}

            if not hasattr(func, "__req_options__"):
                func.__req_options__ = []
            
            if not hasattr(func, "__opt_options__"):
                func.__opt_options__ = []
            
            field: OptionField

            for field in cls.__dict__:
                if isinstance(cls.__dict__[field], OptionField):
                    if field.flag_short in func.__flags_short__:
                        raise ValueError(f"Duplicate short flag: {field.flag_short}")
                    
                    if field.flag_long in func.__flags_long__:
                        raise ValueError(f"Duplicate long flag: {field.flag_long}")
                    
                    if help_fill is not None:
                        field = field.instantiate(help_fill)

                    if field.required:
                        func.__req_options__.append(field)
                    else:
                        func.__opt_options__.append(field)

            return func

        return decorator





