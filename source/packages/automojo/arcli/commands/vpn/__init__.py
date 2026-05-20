"""
    VPN command package — registers the leaf modules on import.
"""

from automojo.arcli.commands.vpn.vpngroup import vpn_group, build_vpn_group
from automojo.arcli.commands.vpn.mintauthkeycommand import (
    mint_authkey_command, build_mint_authkey_command,
)
from automojo.arcli.commands.vpn.peerscommand import (
    peers_command, build_peers_command,
)
from automojo.arcli.commands.vpn.statuscommand import (
    status_command, build_status_command,
)


def register_vpn_commands(*, root):
    """
        Attaches a freshly constructed vpn command group with all three leaf
        subcommands to the supplied root :class:`EntryCommand`.

        :param root: The arcli root EntryCommand.

        :returns: The configured vpn group command.
    """
    group = build_vpn_group()
    group.add_command(build_mint_authkey_command())
    group.add_command(build_peers_command())
    group.add_command(build_status_command())
    root.add_command(group)

    rtnval = group
    return rtnval


__all__ = [
    "vpn_group",
    "mint_authkey_command",
    "peers_command",
    "status_command",
    "register_vpn_commands",
]
