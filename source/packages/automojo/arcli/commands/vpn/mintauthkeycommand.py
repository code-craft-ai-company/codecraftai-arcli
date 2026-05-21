"""
    .. module:: mintauthkeycommand
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: ``arcli vpn mint-authkey`` leaf command.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Automation Mojo LLC"
__credits__ = []


import os
import stat
import sys

from typing import List, Optional

from automojo.arcli import decorators
from automojo.arcli.model.fields.optionfield import OptionMode

from automojo.arcli.commands.common.aspectsfactory import build_default_vpn_aspects
from automojo.arcli.commands.vpn.providerresolver import resolve_vpn_provider
from automojo.arcli.commands.vpn.renderers import render_authkey


def _write_authkey_to_restricted_file(*, path: str, key: str) -> None:
    """
        Write a minted auth key to ``path`` with owner-only (0600)
        permissions so the secret does not land in shell history or a
        world-readable file.

        :param path: The destination file path.
        :param key: The minted auth key to persist.
    """
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    mode = stat.S_IRUSR | stat.S_IWUSR
    fd = os.open(path, flags, mode)
    try:
        os.write(fd, key.encode("utf-8"))
        os.write(fd, os.linesep.encode("utf-8"))
    finally:
        os.close(fd)

    return


def _mint_authkey_body(provider: str, ephemeral: bool, reusable: bool,
                        tag: Optional[List[str]], ttl_seconds: str,
                        show_secret: bool, out_file: Optional[str]):
    """
        Mints an auth key.

        :param provider: ``tailscale`` or ``twingate``.
        :param ephemeral: When True the key is single-use ephemeral.
        :param reusable: When True the key is reusable.
        :param tag: List of tag strings to attach to the key.
        :param ttl_seconds: TTL of the minted key in seconds.
        :param show_secret: When True the minted key is printed to stdout.
        :param out_file: Optional path to write the minted key to with
            owner-only permissions.
    """
    if show_secret is not True and (out_file is None or len(out_file) == 0):
        sys.stderr.write(
            "Refusing to emit a minted auth key. Pass --show-secret to print "
            "it to stdout or --out-file=<path> to write it to a restricted "
            "file.\n"
        )
        sys.exit(2)

    try:
        ttl_int = int(ttl_seconds)
    except ValueError:
        sys.stderr.write("--ttl-seconds must be an integer\n")
        sys.exit(2)

    tags_list: List[str] = []
    if tag is not None:
        tags_list = list(tag)

    try:
        _, control_plane = resolve_vpn_provider(provider_name=provider)
    except ValueError as verr:
        sys.stderr.write("{}\n".format(str(verr)))
        sys.exit(2)

    if control_plane is None:
        sys.stderr.write("No control plane configured for provider '{}'\n".format(provider))
        sys.exit(2)

    aspects = build_default_vpn_aspects()
    key = control_plane.mint_authkey(reusable=reusable, ephemeral=ephemeral,
                                     tags=tags_list, ttl_seconds=ttl_int,
                                     aspects=aspects)

    if out_file is not None and len(out_file) > 0:
        _write_authkey_to_restricted_file(path=out_file, key=key)
        if ephemeral is not True:
            sys.stderr.write("WARNING: This auth key is NOT ephemeral.\n")
        print("Auth key written to {} (owner-readable only).".format(out_file))

    if show_secret is True:
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
    @decorators.option("--show-secret/--no-show-secret", alias="show_secret", default=False)
    @decorators.option("--out-file", alias="out_file", default=None)
    @decorators.command("mint-authkey")
    def mint_authkey_cmd(provider: str, ephemeral: bool, reusable: bool,
                         tag: Optional[List[str]], ttl_seconds: str,
                         show_secret: bool, out_file: Optional[str]):
        _mint_authkey_body(provider, ephemeral, reusable, tag, ttl_seconds,
                           show_secret, out_file)
        return

    rtnval = mint_authkey_cmd
    return rtnval


mint_authkey_command = build_mint_authkey_command()
