"""
    .. module:: mintauthkeycommand
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: ``arcli vpn mint-authkey`` leaf command.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Automation Mojo LLC"
__credits__ = []


import sys

from typing import List, Optional

from automojo.arcli import decorators
from automojo.arcli.model.fields.optionfield import OptionMode

from automojo.arcli.commands.common.aspectsfactory import build_default_vpn_aspects
from automojo.arcli.commands.vpn.providerresolver import resolve_vpn_provider
from automojo.arcli.commands.vpn.renderers import render_authkey


def _mint_authkey_body(provider: str, ephemeral: bool, reusable: bool,
                        tag: Optional[List[str]], ttl_seconds: str):
    """
        Mints an auth key.

        :param provider: ``tailscale`` or ``twingate``.
        :param ephemeral: When True the key is single-use ephemeral.
        :param reusable: When True the key is reusable.
        :param tag: List of tag strings to attach to the key.
        :param ttl_seconds: TTL of the minted key in seconds.
    """
    try:
        ttl_int = int(ttl_seconds)
    except ValueError:
        sys.stderr.write("--ttl-seconds must be an integer\n")
        sys.exit(2)
        return

    tags_list: List[str] = []
    if tag is not None:
        tags_list = list(tag)

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
    key = control_plane.mint_authkey(reusable=reusable, ephemeral=ephemeral,
                                     tags=tags_list, ttl_seconds=ttl_int,
                                     aspects=aspects)

    rendered = render_authkey(key=key, ephemeral=ephemeral)
    print(rendered)
    return


def build_mint_authkey_command():
    """
        Build a fresh ``mint-authkey`` Command instance.

        :returns: A new Command for ``vpn mint-authkey``.
    """
    @decorators.option("--provider", required=True)
    @decorators.option("--ephemeral/--no-ephemeral", alias="ephemeral", default=True)
    @decorators.option("--reusable/--no-reusable", alias="reusable", default=False)
    @decorators.option("--tag", mode=OptionMode.Multiple)
    @decorators.option("--ttl-seconds", default="900")
    @decorators.command("mint-authkey")
    def mint_authkey_cmd(provider: str, ephemeral: bool, reusable: bool,
                         tag: Optional[List[str]], ttl_seconds: str):
        _mint_authkey_body(provider, ephemeral, reusable, tag, ttl_seconds)
        return

    rtnval = mint_authkey_cmd
    return rtnval


mint_authkey_command = build_mint_authkey_command()
