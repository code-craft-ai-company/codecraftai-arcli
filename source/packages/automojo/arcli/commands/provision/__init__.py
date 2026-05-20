"""
    Provision command package — registers leaf modules on import.
"""

from automojo.arcli.commands.provision.provisiongroup import (
    provision_group, build_provision_group,
)
from automojo.arcli.commands.provision.plancommand import (
    plan_command, build_plan_command,
)
from automojo.arcli.commands.provision.applycommand import (
    apply_command, build_apply_command,
)
from automojo.arcli.commands.provision.destroycommand import (
    destroy_command, build_destroy_command,
)
from automojo.arcli.commands.provision.inventorycommand import (
    inventory_command, build_inventory_command,
)


def register_provision_commands(*, root):
    """
        Attaches a freshly constructed provision command group with all four
        leaf subcommands to the supplied root :class:`EntryCommand`.

        :param root: The arcli root EntryCommand.

        :returns: The configured provision group command.
    """
    group = build_provision_group()
    group.add_command(build_plan_command())
    group.add_command(build_apply_command())
    group.add_command(build_destroy_command())
    group.add_command(build_inventory_command())
    root.add_command(group)

    rtnval = group
    return rtnval


__all__ = [
    "provision_group",
    "plan_command",
    "apply_command",
    "destroy_command",
    "inventory_command",
    "register_provision_commands",
]
