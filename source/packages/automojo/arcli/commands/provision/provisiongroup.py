"""
    .. module:: provisiongroup
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: The ``provision`` GroupingCommand for the arcli command tree.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Automation Mojo LLC"
__credits__ = []


from automojo.arcli import decorators


def build_provision_group():
    """
        Build a fresh ``provision`` GroupingCommand.

        :returns: A new GroupingCommand named ``provision``.
    """
    @decorators.group("provision")
    def provision_grp():
        return

    rtnval = provision_grp
    return rtnval


provision_group = build_provision_group()
