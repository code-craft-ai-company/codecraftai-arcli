
from typing import Callable, Type, Union

import collections

from automojo.errors.exceptions import SemanticError

from automojo.arcli.model.argfield import ArgField
from automojo.arcli.model.optionfield import OptionField
from automojo.arcli.model.optiongroup import OptionGroup

class Command:

    def __init__(self, name: str, callable: Callable):
        self._name = name
        self._callable = callable

        self._flags_short = {}
        self._flags_long = {}

        self._required_options = {"*": []}
        self._optional_options = {"*": []}
        self._arguments = []

        self._parameters = collections.OrderedDict()

        self._option_groups = {}
        return

    @property
    def callable(self) -> str:
        return self._callable

    @property
    def name(self) -> str:
        return self._name

    def add_argument(self, arg: ArgField):
        self._arguments.append(arg)

        self._add_parameter(arg)
        return

    def add_option(self, option: OptionField, group_name: str = "*"):
        
        flag_short = option.flag_short
        flag_long = option.flag_long
        required = option.required

        if flag_short in self._flags_short:
            raise ValueError(f"Duplicate short flag: {flag_short}")
        
        self._flags_short[flag_short] = True
        
        if flag_long in self._flags_long:
            raise ValueError(f"Duplicate long flag: {flag_long}")
        
        self._flags_long[flag_long] = True

        if required:
            default_required_group = self._required_options[group_name]
            default_required_group.append(option)
        else:
            default_optional_group = self._optional_options[group_name]
            default_optional_group.append(option)

        self._add_parameter(option)
        
        return

    def add_option_group(self, option_group: Type[OptionGroup]):

        group_name = OptionGroup.name
        
        field: OptionField

        for field_name, field_obj in option_group.__dict__.items():
            if isinstance(field_obj, OptionField):
                field_obj.assign_alias_if_not_set(field_name)
                self.add_option(field_obj, group_name=group_name)
    
        self._option_groups[group_name] = option_group

        return
    
    def _add_parameter(self, param: Union[ArgField, OptionField]):
        
        alias = param.alias

        if alias in self._parameters:
            errmsg = "Duplicate alias found for parameter."
            raise SemanticError(errmsg)

        self._parameters[alias] = param

        return

    def _resolve_command_expectations():
        
        return