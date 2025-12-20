

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []

from typing import Dict, OrderedDict, Generator, List, Tuple, Union, TYPE_CHECKING

import collections
import shlex


from automojo.errors.exceptions import SemanticError

from automojo.arcli.model.parameters.parameterbase import ParameterBase
from automojo.arcli.model.parameters.booleanparameter import BooleanParameter

from automojo.arcli.model.fields.argfield import ArgField
from automojo.arcli.model.fields.optionfield import OptionField, OptionMode
from automojo.arcli.model.fields.trapfield import TrapField


if TYPE_CHECKING:
    from automojo.arcli.model.command import Command


def split_option_component(cmd: str) -> List[str]:
    """
        Splits a command string into a list of tokens, handling quoted strings and escaped characters.

        :param cmd: The command string to be split.
        
        :return: A list of tokens.
    """
    
    tokens = None

    eq_index = cmd.find("=")

    if eq_index > -1:
        tokens = [cmd[:eq_index], "=", cmd[eq_index + 1:]]
    else:
        tokens = [cmd]

    return tokens


class ProgressiveOptionParser:

    def __init__(self, args: List[str]):
        self._args = args
        self._index_cursor = 0
        self._arg_components = args[1:]
        return

    def parse_parameters_for_command(self, command: "Command") -> OrderedDict[str, Union[ArgField, OptionField]]:
        """
        """

        parameter_table = collections.OrderedDict()

        cname = command.name
 
        # This table is used when matching command line flags with the options they
        # correspond with
        flags_lookup_table = command.flags_lookup_table

        # Process options until we reach something without a flag
        nxtopt_field: OptionField
        for nxtopt_flag, nxtopt_value in self._next_option(flags_lookup_table):
            nxtopt_field = flags_lookup_table[nxtopt_flag]

            if isinstance(nxtopt_field, TrapField):
                nxtopt_field.call_trap_callback()
                exit(0) # We only allow one trap to be hit at any given time, then we exit
            elif nxtopt_value is not None:
                nxtopt_field.fill_token(nxtopt_value)
            else:
                print("Encountered 'None' option token.")

        # Once we reach a component that is not an option match it to
        # args.
        argument_components: List[str] = self._collect_arguments(command)
        argument_fields = [af for af in command.arguments]


        # Arguments are not considered optional, if an argument is not passed then 
        if len(argument_components) > len(command.arguments):
            errmsg = f"The number of arguments provided does not match the number of arguments allowed to the '{cname}' command."
            raise SemanticError(errmsg)
        
        elif len(argument_components) == len(command.arguments):

            for argfield in argument_fields:
                argcomp = argument_components.pop(0)
                argfield.fill_token(argcomp)

        else:

            for argcomp in argument_components:
                argfield = argument_fields.pop(0)
                argfield.fill_token(argcomp)
            
            # All the remaining unfilled arguments must be optional with defaults or we have to
            # fail
            for argfield in argument_fields:
                if argfield.required:
                    errmsg = "Command has required arguments that were not filled."
                    raise SemanticError(errmsg)

        for param_obj in command.parameters:
            parameter_table[param_obj.alias] =  param_obj

        return parameter_table


    def _collect_arguments(self, command: "Command") -> List[str]:
        """
            Walk through the argument parameters until we encounter a commandline component that
            matches a child group or action name.
        """
        arguments = []

        if not command.has_children:
            # If the command does not have any children, then all the remaining command components
            # are considered arguments.

            while self._index_cursor < len(self._arg_components):

                nxtarg: str = self._arg_components[self._index_cursor]
                arguments.append(nxtarg)

                self._index_cursor += 1

        else:
            # If the command has children, we process command components until we encounder the name
            # of a child command.
            
            while self._index_cursor < len(self._arg_components):

                nxtarg: str = self._arg_components[self._index_cursor]

                if command.has_child_command(nxtarg):
                    break
                
                arguments.append(nxtarg)

                self._index_cursor += 1

        return arguments


    def _next_option(self, flags_lookup_table: Dict[str, OptionField]) -> Generator[OptionField, None, None]:
        """
            Iterate through the options parameters until we encounter a commandline component
            that does not start with '-' or '--'.
        """

        while self._index_cursor < len(self._arg_components):

            nxtarg: str = self._arg_components[self._index_cursor]
            if not nxtarg.startswith("-"):
                raise StopIteration()

            nxtopt_flag, nxtopt_value = self._read_option_from_tokens(flags_lookup_table)

            if nxtopt_flag is not None and nxtopt_value is not None:
                yield nxtopt_flag, nxtopt_value
            else:
                raise StopIteration()
            
            self._index_cursor += 1

    def _read_option_from_tokens(self, flags_lookup_table: Dict[str, OptionField]) -> Tuple[str, str]:

        nxtarg: str = self._arg_components[self._index_cursor]

        comp_flag = None
        comp_val = None

        pieces = split_option_component(nxtarg)

        if len(pieces) == 1:
            comp_flag = nxtarg

            optfield = flags_lookup_table[comp_flag]
            if isinstance(optfield, TrapField):
                comp_val = ...
            else:
                if optfield.ptype == BooleanParameter:
                    if comp_flag == optfield.flag_long:
                        comp_val = True
                    else:
                        comp_val = False
                elif optfield.mode == OptionMode.Counter:
                    comp_val = 1

        elif len(pieces) == 3 and pieces[1] == '=':
            comp_flag = pieces[0]
            comp_val = pieces[2]

        else:
            errmsg = f"Parse error processing arg '{nxtarg}'"
            raise SemanticError(errmsg)

        return comp_flag, comp_val

    

    