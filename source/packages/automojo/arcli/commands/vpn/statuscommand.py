"""
    .. module:: statuscommand
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: ``arcli vpn status`` leaf command.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Automation Mojo LLC"
__credits__ = []


import sys

from automojo.arcli import decorators

from automojo.arcli.commands.common.aspectsfactory import build_default_vpn_aspects
from automojo.arcli.commands.vpn.providerresolver import resolve_vpn_provider
from automojo.arcli.commands.vpn.renderers import render_status


def _status_body(provider: str, format: str):
    """
        Reports the local VPN client's status.

        :param provider: ``tailscale`` or ``twingate``.
        :param format: ``text`` or ``json``.
    """
    try:
        client, _ = resolve_vpn_provider(provider_name=provider)
    except ValueError as verr:
        sys.stderr.write("{}\n".format(str(verr)))
        sys.exit(2)
        return

    if client is None:
        sys.stderr.write("No VPN client configured for provider '{}'\n".format(provider))
        sys.exit(2)
        return

    aspects = build_default_vpn_aspects()
    status = client.status(aspects=aspects)

    rendered = render_status(status=status, fmt=format)
    print(rendered)
    return


def build_status_command():
    """
        Build a fresh ``status`` Command instance.

        :returns: A new Command for ``vpn status``.
    """
    @decorators.option("--provider", required=True)
    @decorators.option("--format", default="text")
    @decorators.command("status")
    def status_cmd(provider: str, format: str):
        _status_body(provider, format)
        return

    rtnval = status_cmd
    return rtnval


status_command = build_status_command()
