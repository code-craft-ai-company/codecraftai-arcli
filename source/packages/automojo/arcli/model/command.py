
from typing import Callable, Dict, List, Type, Union

import collections
import inspect

from automojo.errors.exceptions import SemanticError

from automojo.arcli.model.argfield import ArgField
from automojo.arcli.model.clicontext import CliContext
from automojo.arcli.model.optionfield import OptionField
from automojo.arcli.model.optiongroup import OptionGroup

from automojo.arcli.parsing import ProgressiveOptionParser

class Command:

    def __init__(self, name: str, callable: Callable):
        self._name = name
        self._callable = callable

        self._flags_short = {}
        self._flags_long = {}

        self._options = collections.OrderedDict()
        self._arguments = []

        self._parameters = collections.OrderedDict()

        self._option_groups = {}

        self._callargs = []
        return

    @property
    def arguments(self) -> List[ArgField]:
        return self._arguments

    @property
    def callable(self) -> str:
        return self._callable

    @property
    def flags_lookup_table(self) -> Dict[str, OptionField]:
        lookup_table = {}
        lookup_table.update(self._flags_short)
        lookup_table.update(self._flags_long)
        return lookup_table

    @property
    def has_children(self) -> bool:
        return False

    @property
    def name(self) -> str:
        return self._name

    @property
    def options(self) -> List[OptionField]:
        return self._options
    
    @property
    def parameters(self) -> List[Union[ArgField, OptionField]]:
        rtnval = [fobj for fobj in self._parameters.values()]
        return rtnval

    def add_argument(self, arg: ArgField):
        self._arguments.append(arg)

        self._add_parameter(arg)
        return

    def add_option(self, option: OptionField, group_name: str = "*"):
        
        flag_short = option.flag_short
        flag_long = option.flag_long
        required = option.required

        if flag_short is not None and flag_short in self._flags_short:
            raise ValueError(f"Duplicate short flag: {flag_short}")
        
        self._flags_short[flag_short] = option
        
        if flag_long in self._flags_long:
            raise ValueError(f"Duplicate long flag: {flag_long}")
        
        self._flags_long[flag_long] = option

        param_name = option.alias

        self._options[param_name] = option

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
    
    def call_command(self):

        self._callable(*self._callargs)

        return

    def has_child_command(self, cmdname: str):
        """
            Determines if this command has a child command with the given name.
        """
        return False

    def lookup_field_by_alias(self, alias: str):

        field_obj = None

        if alias in self._options:
            field_obj = self._options[alias]
        
        return

    def prepare_callargs(self, context: CliContext, parser: ProgressiveOptionParser):

        callargs = []

        sigspec = inspect.signature(self._callable)

        argnames = [aname for aname in sigspec.parameters.keys()]
        if argnames[0] == 'context':
            callargs.append(context)

        parameter_table = parser.parse_parameters_for_command(self)

        for argn in argnames:
            if argn in parameter_table:
                param = parameter_table[argn]
                argv = param.get_value()
                callargs.append(argv)
            else:
                fname = self._callable.__name__
                errmsg = f"The {argn} parameter for function '{fname}' could not be found."
                raise SemanticError(errmsg)

        return
    
    def _add_parameter(self, param: Union[ArgField, OptionField]):
        
        alias = param.alias

        if alias in self._parameters:
            errmsg = "Duplicate alias found for parameter."
            raise SemanticError(errmsg)

        self._parameters[alias] = param

        return