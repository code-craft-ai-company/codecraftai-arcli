"""
    .. module:: renderers
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Renderers for the VPN CLI subcommands.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Automation Mojo LLC"
__credits__ = []


import json
import os

from typing import Any, List


_TEXT_FORMAT = "text"
_JSON_FORMAT = "json"

ALLOWED_FORMATS = (_TEXT_FORMAT, _JSON_FORMAT)


def render_authkey(*, key: str, ephemeral: bool) -> str:
    """
        Render a minted auth key.  When ``ephemeral`` is False a warning is
        prepended.

        :param key: The minted auth key.
        :param ephemeral: True when the minted key is ephemeral.

        :returns: The rendered text.
    """
    lines: List[str] = []
    if ephemeral is not True:
        lines.append("WARNING: This auth key is NOT ephemeral.")
    lines.append(key)

    rtnval = os.linesep.join(lines)
    return rtnval


def _device_row(*, device: Any) -> dict:
    """
        Project a :class:`VPNDeviceRecord` to a plain dictionary.

        :param device: The device record.

        :returns: A dictionary with the displayed fields.
    """
    row = {
        "device_id": getattr(device, "device_id", None),
        "hostname": getattr(device, "hostname", None),
        "overlay_address": getattr(device, "overlay_address", None),
        "tags": list(getattr(device, "tags", []) or []),
        "os": getattr(device, "os", None),
        "last_seen": getattr(device, "last_seen", None),
    }
    return row


def render_peers(*, devices: List[Any], fmt: str) -> str:
    """
        Render a list of :class:`VPNDeviceRecord` objects.

        :param devices: The device records.
        :param fmt: ``text`` or ``json``.

        :returns: The rendered text.
        :raises: ValueError
    """
    if fmt not in ALLOWED_FORMATS:
        err_msg = "Unknown format '{}'.  Allowed: {}".format(fmt, ALLOWED_FORMATS)
        raise ValueError(err_msg)

    rows = [_device_row(device=device) for device in devices]

    if fmt == _JSON_FORMAT:
        rtnval = json.dumps(rows, indent=2, sort_keys=True, default=str)
        return rtnval

    lines = ["{:<24} {:<24} {:<18} {:<32} {}".format(
        "DEVICE_ID", "HOSTNAME", "OVERLAY", "TAGS", "LAST_SEEN"
    )]
    for row in rows:
        overlay = row["overlay_address"]
        if overlay is None:
            overlay = "-"
        tags_str = ",".join(row["tags"]) if len(row["tags"]) > 0 else "-"
        last_seen_str = "-" if row["last_seen"] is None else str(row["last_seen"])
        lines.append("{:<24} {:<24} {:<18} {:<32} {}".format(
            str(row["device_id"]) if row["device_id"] is not None else "-",
            str(row["hostname"]) if row["hostname"] is not None else "-",
            overlay, tags_str, last_seen_str,
        ))

    rtnval = os.linesep.join(lines)
    return rtnval


def render_status(*, status: Any, fmt: str) -> str:
    """
        Render a :class:`VPNStatus` object.

        :param status: The status record.
        :param fmt: ``text`` or ``json``.

        :returns: The rendered text.
        :raises: ValueError
    """
    if fmt not in ALLOWED_FORMATS:
        err_msg = "Unknown format '{}'.  Allowed: {}".format(fmt, ALLOWED_FORMATS)
        raise ValueError(err_msg)

    row = {
        "connected": getattr(status, "connected", None),
        "backend_state": getattr(status, "backend_state", None),
        "self_address": getattr(status, "self_address", None),
        "hostname": getattr(status, "hostname", None),
        "tags": list(getattr(status, "tags", []) or []),
        "provider": getattr(status, "provider", None),
    }

    if fmt == _JSON_FORMAT:
        rtnval = json.dumps(row, indent=2, sort_keys=True, default=str)
        return rtnval

    lines = ["VPNStatus:"]
    lines.append("    provider:      {}".format(row["provider"]))
    lines.append("    connected:     {}".format(row["connected"]))
    lines.append("    backend_state: {}".format(row["backend_state"]))
    lines.append("    self_address:  {}".format(row["self_address"]))
    lines.append("    hostname:      {}".format(row["hostname"]))
    lines.append("    tags:          {}".format(",".join(row["tags"]) if len(row["tags"]) > 0 else "-"))

    rtnval = os.linesep.join(lines)
    return rtnval
