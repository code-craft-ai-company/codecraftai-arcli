"""
    .. module:: vpngroup
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: The ``vpn`` GroupingCommand for the arcli command tree.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Automation Mojo LLC"
__credits__ = []


from automojo.arcli import decorators


def build_vpn_group():
    """
        Build a fresh ``vpn`` GroupingCommand.

        :returns: A new GroupingCommand named ``vpn``.
    """
    @decorators.group("vpn")
    def vpn_grp():
        return

    rtnval = vpn_grp
    return rtnval


vpn_group = build_vpn_group()
