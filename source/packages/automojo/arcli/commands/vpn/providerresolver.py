"""
    .. module:: providerresolver
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: VPN provider resolution helper for the arcli VPN commands.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Automation Mojo LLC"
__credits__ = []


import os

from typing import Any, Callable, Optional, Tuple


SUPPORTED_PROVIDERS = ("tailscale", "twingate")


_resolver_override: Optional[Callable[..., Tuple[Any, Any]]] = None


def set_provider_resolver(*, resolver: Optional[Callable[..., Tuple[Any, Any]]]) -> None:
    """
        Override the provider resolver used by the VPN subcommands.

        :param resolver: A callable taking ``provider_name`` and returning a
                         ``(client_or_none, control_plane_or_none)`` tuple, or
                         None to restore the default behaviour.
    """
    global _resolver_override
    _resolver_override = resolver
    return


def resolve_vpn_provider(*, provider_name: str) -> Tuple[Any, Any]:
    """
        Resolve the configured ``(IVPNClient?, IVPNControlPlane?)`` pair for
        the named provider.

        :param provider_name: One of ``"tailscale"`` or ``"twingate"``.

        :returns: A tuple ``(client_or_none, control_plane_or_none)``.
        :raises: ValueError when the provider name is not supported.
                 ConfigurationError when the provider is not configured.
    """
    if provider_name not in SUPPORTED_PROVIDERS:
        err_msg_lines = ["Unknown VPN provider."]
        err_msg_lines.append("PROVIDER: {}".format(provider_name))
        err_msg_lines.append("ALLOWED: {}".format(", ".join(SUPPORTED_PROVIDERS)))
        err_msg = os.linesep.join(err_msg_lines)
        raise ValueError(err_msg)

    if _resolver_override is not None:
        rtnval = _resolver_override(provider_name=provider_name)
        return rtnval

    from automojo.errors.exceptions import ConfigurationError

    err_msg_lines = ["No VPN provider resolver is configured."]
    err_msg_lines.append("PROVIDER: {}".format(provider_name))
    err_msg_lines.append("HINT: install a provider resolver via "
                        "automojo.arcli.commands.vpn.providerresolver."
                        "set_provider_resolver(resolver=...)")
    err_msg = os.linesep.join(err_msg_lines)
    raise ConfigurationError(err_msg)
