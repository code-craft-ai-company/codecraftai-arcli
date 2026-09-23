
__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []

import textwrap

from ccai.arcli.model.command import Command
from ccai.arcli.model.groupingcommand import GroupingCommand
from ccai.arcli.model.entrycommand import EntryCommand
from ccai.arcli.model.parameters.booleanparameter import BooleanParameter

class HelpGenerator:
    """
    Generates help text for commands.
    """

    @staticmethod
    def generate_help(command: Command) -> str:
        parts = []

        # 1. Usage
        parts.append(HelpGenerator._generate_usage(command))
        parts.append("")

        # 2. Description
        if command.callable.__doc__:
            doc = textwrap.dedent(command.callable.__doc__).strip()
            parts.append(f"  {doc}")
            parts.append("")

        # 3. Options & Traps
        options_output = HelpGenerator._generate_options(command)
        if options_output:
            parts.append("Options:")
            parts.append(options_output)
            parts.append("")

        # 4. Commands (if GroupingCommand)
        if isinstance(command, GroupingCommand) and command.has_children:
             commands_output = HelpGenerator._generate_commands(command)
             if commands_output:
                 parts.append("Commands:")
                 parts.append(commands_output)
                 parts.append("")

        return "\n".join(parts)

    @staticmethod
    def _generate_usage(command: Command) -> str:
        prog_name = command.name
        if isinstance(command, EntryCommand):
            prog_name = command.program_name

        usage_parts = [prog_name]

        if command.options or command.traps:
            usage_parts.append("[OPTIONS]")

        if isinstance(command, GroupingCommand) and command.has_children:
            usage_parts.append("COMMAND [ARGS]...")
        else:
            for arg in command.arguments:
                name = arg.name.upper()
                if not arg.required:
                    usage_parts.append(f"[{name}]")
                else:
                    usage_parts.append(name)

        return f"Usage: {' '.join(usage_parts)}"

    @staticmethod
    def _generate_options(command: Command) -> str:
        items = []

        # Traps
        for trap in command.traps:
             flags = []
             if trap.flag_short: flags.append(trap.flag_short)
             if trap.flag_long: flags.append(trap.flag_long)
             items.append((", ".join(flags), trap.help or ""))

        # Options
        for option in command.options.values():
             flags = []
             if option.flag_short: flags.append(option.flag_short)
             if option.flag_long: flags.append(option.flag_long)

             flag_str = ", ".join(flags)

             # Add type info if not boolean
             if option.ptype != BooleanParameter:
                  type_name = "TEXT"
                  if option.ptype and hasattr(option.ptype, "__name__"):
                      type_name = option.ptype.__name__.upper().replace("PARAMETER", "")
                  flag_str += f" {type_name}"

             items.append((flag_str, option.help or ""))

        if not items:
            return ""

        # Calculate padding
        max_len = max(len(x[0]) for x in items) + 2

        output = []
        for flag_str, help_text in items:
            output.append(f"  {flag_str.ljust(max_len)}{help_text}")

        return "\n".join(output)

    @staticmethod
    def _generate_commands(command: GroupingCommand) -> str:
        items = []
        for name, cmd in command._command_nodes.items():
            doc = ""
            if cmd.callable.__doc__:
                 # Take first line of docstring
                 doc = textwrap.dedent(cmd.callable.__doc__).strip().split("\n")[0]
            items.append((name, doc))

        if not items:
            return ""

        max_len = max(len(x[0]) for x in items) + 2
        output = []
        for name, doc in items:
             output.append(f"  {name.ljust(max_len)}{doc}")

        return "\n".join(output)
