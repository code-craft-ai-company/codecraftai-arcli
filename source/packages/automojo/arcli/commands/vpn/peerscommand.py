"""
    .. module:: peerscommand
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: ``arcli vpn peers`` leaf command.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Automation Mojo LLC"
__credits__ = []


import sys

from automojo.arcli import decorators

from automojo.arcli.commands.common.aspectsfactory import build_default_vpn_aspects
from automojo.arcli.commands.vpn.providerresolver import resolve_vpn_provider
from automojo.arcli.commands.vpn.renderers import render_peers


def _peers_body(provider: str, format: str):
    """
        Lists devices known to the resolved control plane.

        :param provider: ``tailscale`` or ``twingate``.
        :param format: ``text`` or ``json``.
    """
    try:
        _, control_plane = resolve_vpn_provider(provider_name=provider)
    except ValueError as verr:
        sys.stderr.write("{}\n".format(str(verr)))
        sys.exit(2)
        return

    if control_plane is None:
        sys.stderr.write("No control plane configured for provider '{}'\n".format(provider))
        sys.exit(2)
        return

    aspects = build_default_vpn_aspects()
    devices = control_plane.list_devices(aspects=aspects)

    rendered = render_peers(devices=devices, fmt=format)
    print(rendered)
    return


def build_peers_command():
    """
        Build a fresh ``peers`` Command instance.

        :returns: A new Command for ``vpn peers``.
    """
    @decorators.option("--provider", required=True)
    @decorators.option("--format", default="text")
    @decorators.command("peers")
    def peers_cmd(provider: str, format: str):
        _peers_body(provider, format)
        return

    rtnval = peers_cmd
    return rtnval


peers_command = build_peers_command()
