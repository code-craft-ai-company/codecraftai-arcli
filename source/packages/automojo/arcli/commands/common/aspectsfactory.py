"""
    .. module:: aspectsfactory
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Builders for default Aspects objects used by the arcli CLI surface.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Automation Mojo LLC"
__credits__ = []


def build_default_provisioning_aspects(*, dry_run: bool = False, confirm: bool = False):
    """
        Builds the default :class:`ProvisioningAspects` object used by the CLI.

        The import of :class:`ProvisioningAspects` is performed lazily so that
        the arcli command tree can be imported in environments where the
        provisioning package is not installed.

        :param dry_run: When True the engine halts after the PLAN stage.
        :param confirm: When True destructive actions are permitted.

        :returns: A configured ``ProvisioningAspects`` instance.
    """
    from automojo.provisioning.aspects.provisioningaspects import ProvisioningAspects

    aspects = ProvisioningAspects(dry_run=dry_run, confirm=confirm)

    rtnval = aspects
    return rtnval


def build_default_vpn_aspects():
    """
        Builds the default :class:`Aspects` object used by the VPN CLI commands.

        :returns: A configured ``Aspects`` instance.
    """
    from automojo.aspects.aspects import Aspects

    aspects = Aspects()

    rtnval = aspects
    return rtnval
