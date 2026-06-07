"""
    .. module:: renderers
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Renderers for the provisioning CLI subcommands.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


import json
import os

from typing import Any, Dict, List


_TEXT_FORMAT = "text"
_JSON_FORMAT = "json"
_YAML_FORMAT = "yaml"

ALLOWED_FORMATS = (_TEXT_FORMAT, _JSON_FORMAT, _YAML_FORMAT)


def _plan_to_dict(*, plan: Any) -> Dict[str, Any]:
    """
        Convert a plan object to a dictionary.  Accepts objects that already
        expose ``to_dict`` and plain dictionaries.

        :param plan: The plan object to convert.

        :returns: A dictionary representation.
    """
    if isinstance(plan, dict):
        rtnval = plan
        return rtnval

    if hasattr(plan, "to_dict"):
        rtnval = plan.to_dict()
        return rtnval

    rtnval = {"plan": repr(plan)}
    return rtnval


def render_plan(*, plan: Any, fmt: str) -> str:
    """
        Render a MultiVenueProvisioningPlan for stdout.

        :param plan: The plan object.
        :param fmt: One of "text" or "json".

        :returns: The rendered text.
        :raises: ValueError
    """
    if fmt not in ALLOWED_FORMATS:
        err_msg = "Unknown format '{}'.  Allowed: {}".format(fmt, ALLOWED_FORMATS)
        raise ValueError(err_msg)

    plan_dict = _plan_to_dict(plan=plan)

    if fmt == _JSON_FORMAT:
        rtnval = json.dumps(plan_dict, indent=2, sort_keys=True, default=str)
        return rtnval

    lines = ["ProvisioningPlan:"]
    per_venue = plan_dict.get("per_venue_plans", {})
    if len(per_venue) == 0:
        lines.append("    (no venues)")
    for venue_name in sorted(per_venue.keys()):
        lines.append("    venue={}".format(venue_name))
        venue_plan = per_venue[venue_name]
        actions = venue_plan.get("actions", []) if isinstance(venue_plan, dict) else []
        lines.append("        actions: {}".format(len(actions)))

    total_count = plan_dict.get("total_action_count", None)
    if total_count is not None:
        lines.append("    total_actions: {}".format(total_count))

    rtnval = os.linesep.join(lines)
    return rtnval


def render_result(*, result: Any, fmt: str) -> str:
    """
        Render an apply result for stdout.

        :param result: A per-venue results map.
        :param fmt: One of "text" or "json".

        :returns: The rendered text.
        :raises: ValueError
    """
    if fmt not in ALLOWED_FORMATS:
        err_msg = "Unknown format '{}'.  Allowed: {}".format(fmt, ALLOWED_FORMATS)
        raise ValueError(err_msg)

    serialised: Dict[str, Any] = {}
    if isinstance(result, dict):
        for venue_name, venue_result in result.items():
            if hasattr(venue_result, "to_dict"):
                serialised[venue_name] = venue_result.to_dict()
            else:
                serialised[venue_name] = {
                    "created": getattr(venue_result, "created", []),
                    "updated": getattr(venue_result, "updated", []),
                    "skipped": getattr(venue_result, "skipped", []),
                    "errors": getattr(venue_result, "errors", []),
                }

    if fmt == _JSON_FORMAT:
        rtnval = json.dumps(serialised, indent=2, sort_keys=True, default=str)
        return rtnval

    lines = ["ProvisioningResult:"]
    if len(serialised) == 0:
        lines.append("    (no venues)")
    for venue_name in sorted(serialised.keys()):
        venue_dict = serialised[venue_name]
        lines.append("    venue={}".format(venue_name))
        for key in ("created", "updated", "skipped", "errors"):
            collection = venue_dict.get(key, [])
            lines.append("        {}: {}".format(key, len(collection)))

    rtnval = os.linesep.join(lines)
    return rtnval


def render_inventory(*, items: Dict[str, List[Any]], fmt: str) -> str:
    """
        Render an inventory map for stdout.

        :param items: Per-venue inventory map.
        :param fmt: One of "text", "yaml", or "json".

        :returns: The rendered text.
        :raises: ValueError
    """
    if fmt not in ALLOWED_FORMATS:
        err_msg = "Unknown format '{}'.  Allowed: {}".format(fmt, ALLOWED_FORMATS)
        raise ValueError(err_msg)

    serialised: Dict[str, List[Dict[str, Any]]] = {}
    for venue_name, resources in items.items():
        rows: List[Dict[str, Any]] = []
        for resource in resources:
            if hasattr(resource, "to_dict"):
                rows.append(resource.to_dict())
            elif isinstance(resource, dict):
                rows.append(resource)
            else:
                rows.append({
                    "name": getattr(resource, "name", repr(resource)),
                    "kind": getattr(resource, "kind", None),
                })
        serialised[venue_name] = rows

    if fmt == _JSON_FORMAT:
        rtnval = json.dumps(serialised, indent=2, sort_keys=True, default=str)
        return rtnval

    if fmt == _YAML_FORMAT:
        import yaml
        rtnval = yaml.safe_dump(serialised, default_flow_style=False, sort_keys=True)
        return rtnval

    lines = ["Inventory:"]
    if len(serialised) == 0:
        lines.append("    (empty)")
    for venue_name in sorted(serialised.keys()):
        rows = serialised[venue_name]
        lines.append("    venue={} count={}".format(venue_name, len(rows)))
        for row in rows:
            name = row.get("name", "?")
            kind = row.get("kind", "?")
            lines.append("        - kind={} name={}".format(kind, name))

    rtnval = os.linesep.join(lines)
    return rtnval
