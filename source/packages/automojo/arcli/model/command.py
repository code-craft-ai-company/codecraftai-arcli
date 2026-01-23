

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []

from typing import Callable, Dict, List, Optional, Type, Union

import collections
import inspect

from automojo.errors.exceptions import SemanticError

from automojo.arcli.model.fields.argfield import ArgField
from automojo.arcli.model.clicontext import CliContext
from automojo.arcli.model.fields.optionfield import OptionField
from automojo.arcli.model.optiongroup import OptionGroup
from automojo.arcli.model.fields.trapfield import TrapField

from automojo.arcli.parsing import ProgressiveOptionParser

class Command:
    """
        Base class for command-line interface commands.
        
        The Command class provides the foundation for building command-line interface commands
        with support for arguments, options, and traps. It manages the registration and parsing
        of command-line parameters and handles the execution of the associated callable function.
        
        This class serves as the base for more specialized command types and provides the core
        functionality for parameter management, flag handling, and command execution.
    """

    def __init__(self, name: str, callable: Callable):
        """
            Initialize a new Command instance.
            
            :param name: The name of the command
            :param callable: The function to be called when this command is executed
        """
        self._name = name
        self._callable = callable

        self._flags_short = {}
        self._flags_long = {}

        self._traps = []
        self._options = collections.OrderedDict()
        self._arguments = []

        self._parameter_fields = collections.OrderedDict()

        self._option_groups = {}

        self._callargs = []
        
        # Process arguments from decorator
        if hasattr(callable, "__arguments__"):
            for arg_name, arg_field in callable.__arguments__.items():
                self.add_argument(arg_field)

        self.add_trap(TrapField("-h", "--help", trap_callback=self._help_callback, help="Show this message and exit."))
        
        return

    @property
    def arguments(self) -> List[ArgField]:
        """
            Get the list of argument fields for this command.
            
            :returns: List of argument fields registered with this command
        """
        return self._arguments

    @property
    def callable(self) -> Callable:
        """
            Get the callable function associated with this command.
            
            :returns: The callable function that will be executed when this command is invoked
        """
        return self._callable

    @property
    def flags_lookup_table(self) -> Dict[str, OptionField]:
        """
            Get a combined lookup table of all short and long flags.
            
            :returns: Dictionary mapping flag names to their corresponding OptionField objects
        """
        lookup_table = {}
        lookup_table.update(self._flags_short)
        lookup_table.update(self._flags_long)
        return lookup_table

    @property
    def has_children(self) -> bool:
        """
            Check if this command has child commands.
            
            :returns: False for base Command class, may be overridden in subclasses
        """
        return False

    @property
    def name(self) -> str:
        """
            Get the name of this command.
            
            :returns: The command name
        """
        return self._name

    @property
    def options(self) -> List[OptionField]:
        """
            Get the list of option fields for this command.
            
            :returns: List of option fields registered with this command
        """
        return self._options
    
    @property
    def parameters(self) -> List[Union[ArgField, OptionField]]:
        """
            Get all parameters (arguments and options) for this command.
            
            :returns: List of all parameter objects associated with this command
        """
        
        rtnval = []
        
        fobj: Union[ArgField, OptionField]
        for fobj in self._parameter_fields.values():
            param = fobj.get_parameter()
            rtnval.append(param)

        return rtnval

    @property
    def traps(self) -> List[TrapField]:
        """
            Get the list of trap fields for this command.
            
            :returns: Copy of the list of trap fields registered with this command
        """
        rtnval = self._traps.copy()
        return rtnval

    def add_argument(self, arg: ArgField):
        """
            Add an argument field to this command.
            
            :param arg: The argument field to add to this command
        """
        self._arguments.append(arg)

        self._add_parameter(arg)
        return

    def add_option(self, option: OptionField, group_name: str = "*"):
        """
            Add an option field to this command.
            
            This method registers an option with both short and long flag lookups
            and validates that no duplicate flags are being registered.
            
            :param option: The option field to add to this command
            :param group_name: The name of the option group this option belongs to
            
            :raises: ValueError
        """
        
        flag_short = option.flag_short
        flag_long = option.flag_long

        if flag_short is not None and flag_short in self._flags_short:
            raise ValueError(f"Duplicate short flag: {flag_short}")
        
        if flag_short is not None:
            self._flags_short[flag_short] = option
        
        if flag_long in self._flags_long:
            raise ValueError(f"Duplicate long flag: {flag_long}")
        
        self._flags_long[flag_long] = option

        param_name = option.alias

        self._options[param_name] = option

        self._add_parameter(option)
        
        return

    def add_trap(self, trap: TrapField, group_name: str = "*"):
        """
            Add a trap field to this command.
            
            Trap options are high priority flags that perform a task and halt execution.
            They are not passed to the command callback and are handled during parameter parsing.
            
            :param trap: The trap field to add to this command
            :param group_name: The name of the option group this trap belongs to
            
            :raises: ValueError
        """
        
        flag_short = trap.flag_short
        flag_long = trap.flag_long

        if flag_short is not None and flag_short in self._flags_short:
            raise ValueError(f"Duplicate short flag: {flag_short}")
        
        if flag_short is not None:
            self._flags_short[flag_short] = trap
        
        if flag_long in self._flags_long:
            raise ValueError(f"Duplicate long flag: {flag_long}")
        
        self._flags_long[flag_long] = trap

        self._traps.append(trap)

        # Trap options are simple high priority flags that perform a task and hault execution, they are not
        # passed on to the command callback, they will be handled during parameter parsing.

        return

    def add_option_group(self, option_group: Type[OptionGroup], help_fill: Optional[Dict[str, str]] = None):
        """
            Add an option group to this command.
            
            This method processes all OptionField objects in the option group class
            and registers them with this command.
            
            :param option_group: The option group class containing OptionField objects
        """
        # Create an instance of the option group
        group_instance = option_group()
        group_name = group_instance.name
        
        if help_fill is None:
            help_fill = {}
        
        field: OptionField
        for field_name, field_obj in group_instance.__class__.__dict__.items():
            if isinstance(field_obj, OptionField):
                # Clone the field to avoid shared state between commands
                cloned_field = field_obj.clone_and_fill(field_name, help_fill)
                cloned_field.assign_alias_if_not_set(field_name)
                self.add_option(cloned_field, group_name=group_name)

        self._option_groups[group_name] = group_instance

        return
    
    def call_command(self):
        """
            Execute the callable function associated with this command.
            
            This method invokes the command's callable function using the prepared
            call arguments that were set up during parameter parsing.
        """

        self._callable(*self._callargs)

        return

    def has_child_command(self, cmdname: str):
        """
            Determine if this command has a child command with the given name.
            
            :param cmdname: The name of the child command to check for
            
            :returns: False for base Command class, may be overridden in subclasses
        """
        return False

    def lookup_field_by_alias(self, alias: str):
        """
            Look up a field object by its alias name.
            
            :param alias: The alias name to search for
            
            :returns: The OptionField object if found, None otherwise
        """

        field_obj = None

        if alias in self._options:
            field_obj = self._options[alias]
        
        return field_obj

    def prepare_callargs(self, context: CliContext, parser: ProgressiveOptionParser):
        """
            Prepare the call arguments for command execution.
            
            This method inspects the callable function's signature and builds the
            appropriate argument list from the parsed parameters and context.
            
            :param context: The CLI context object
            :param parser: The progressive option parser containing parsed parameters
            
            :raises: SemanticError
        """

        callargs = []

        sigspec = inspect.signature(self._callable)

        argnames = [aname for aname in sigspec.parameters.keys()]
        
        # Track if we've handled context parameter
        context_handled = False
        if len(argnames) > 0 and argnames[0] == 'context':
            callargs.append(context)
            context_handled = True

        parameter_table = parser.parse_parameters_for_command(self, context)

        for argn in argnames:
            # Skip context if we already handled it
            if argn == 'context' and context_handled:
                continue
                
            if argn in parameter_table:
                param = parameter_table[argn]
                argv = param.get_value()
                callargs.append(argv)
            else:
                fname = self._callable.__name__
                errmsg = f"The {argn} parameter for function '{fname}' could not be found."
                raise SemanticError(errmsg)

        self._callargs = callargs

        return
    
    def _add_parameter(self, param: Union[ArgField, OptionField]):
        """
            Add a parameter field to the internal parameter collection.
            
            This is a private method used internally to register parameter fields
            and validate that no duplicate aliases are being registered.
            
            :param param: The parameter field to add
            
            :raises: SemanticError
        """
        
        alias = param.alias

        if alias in self._parameter_fields:
            errmsg = "Duplicate alias found for parameter."
            raise SemanticError(errmsg)

        self._parameter_fields[alias] = param

        return

    def _help_callback(self):
        """
            Callback function for the help trap.

            Generates and displays the help message for this command, then exits.
        """
        from automojo.arcli.helpgenerator import HelpGenerator
        help_text = HelpGenerator.generate_help(self)
        print(help_text)
        exit(0)
