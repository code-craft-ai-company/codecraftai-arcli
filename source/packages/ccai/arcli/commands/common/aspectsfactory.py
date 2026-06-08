"""
    .. module:: aspectsfactory
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Builders for default Aspects objects used by the arcli CLI surface.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
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
    from ccai.provisioning.aspects.provisioningaspects import ProvisioningAspects

    aspects = ProvisioningAspects(dry_run=dry_run, confirm=confirm)

    rtnval = aspects
    return rtnval


DEFAULT_VPN_COMMAND_TIMEOUT_SECONDS = 30
DEFAULT_VPN_STATUS_REFRESH_SECONDS = 10


class VpnClientAspects:
    """
        Behaviour-control aspects for the VPN interop clients invoked by the
        ``arcli vpn`` subcommands.

        The interop VPN clients (``TailscaleClient`` / ``TwingateClient``)
        read VPN-specific aspect fields — ``dry_run``, ``elevated``,
        ``command_timeout_seconds`` and ``status_refresh_seconds`` — that a
        plain :class:`Aspects` object does not carry. Passing a plain
        :class:`Aspects` instance therefore raised ``AttributeError`` inside
        the client (audit IL-H5). This carrier exposes exactly those fields.
    """

    def __init__(self, *, dry_run: bool = False, elevated: bool = False,
                 command_timeout_seconds: float = DEFAULT_VPN_COMMAND_TIMEOUT_SECONDS,
                 status_refresh_seconds: float = DEFAULT_VPN_STATUS_REFRESH_SECONDS):
        """
            Initialize a set of VPN client aspects.

            :param dry_run: When True the client SHALL NOT invoke commands.
            :param elevated: When True write operations SHALL run elevated.
            :param command_timeout_seconds: Per-command timeout in seconds.
            :param status_refresh_seconds: Maximum age of a cached status.
        """
        self._dry_run = dry_run
        self._elevated = elevated
        self._command_timeout_seconds = command_timeout_seconds
        self._status_refresh_seconds = status_refresh_seconds
        return

    @property
    def dry_run(self) -> bool:
        """
            Whether the call is in dry-run mode.

            :returns: True when dry-run is requested.
        """
        rtnval = self._dry_run
        return rtnval

    @property
    def elevated(self) -> bool:
        """
            Whether write operations SHALL be run elevated.

            :returns: True when elevation is requested.
        """
        rtnval = self._elevated
        return rtnval

    @property
    def command_timeout_seconds(self) -> float:
        """
            Per-command timeout in seconds.

            :returns: A timeout value in seconds.
        """
        rtnval = self._command_timeout_seconds
        return rtnval

    @property
    def status_refresh_seconds(self) -> float:
        """
            Maximum age of a cached status snapshot in seconds.

            :returns: A refresh window in seconds.
        """
        rtnval = self._status_refresh_seconds
        return rtnval


def build_default_vpn_aspects():
    """
        Builds the default VPN-client aspects object used by the ``arcli vpn``
        CLI commands.

        Returns a :class:`VpnClientAspects` instance, which carries the
        VPN-specific aspect fields (``dry_run``, ``elevated``,
        ``command_timeout_seconds``, ``status_refresh_seconds``) the interop
        VPN clients read. A plain :class:`Aspects` object lacks those fields
        and produced an ``AttributeError`` at runtime (audit IL-H5).

        :returns: A configured ``VpnClientAspects`` instance.
    """
    aspects = VpnClientAspects()

    rtnval = aspects
    return rtnval
