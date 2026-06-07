"""
    .. module:: inventorycommand
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: ``arcli provision inventory <spec.yaml>`` leaf command.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


import sys

from ccai.arcli import decorators

from ccai.arcli.commands.common.aspectsfactory import (
    build_default_provisioning_aspects,
)
from ccai.arcli.commands.provision.enginefactory import build_engine
from ccai.arcli.commands.provision.renderers import render_inventory
from ccai.arcli.commands.provision.specloader import load_provisioning_spec


def _inventory_body(spec_path: str, format: str):
    """
        Loads the spec and renders the inventory map.

        :param spec_path: Filesystem path to the spec YAML file.
        :param format: ``yaml``, ``text``, or ``json``.
    """
    try:
        spec = load_provisioning_spec(spec_path=spec_path)
    except FileNotFoundError as ferr:
        sys.stderr.write("{}\n".format(str(ferr)))
        sys.exit(2)

    aspects = build_default_provisioning_aspects()
    engine = build_engine(spec=spec)
    inventory_map = engine.inventory(aspects=aspects)

    rendered = render_inventory(items=inventory_map, fmt=format)
    print(rendered)
    return


def build_inventory_command():
    """
        Build a fresh ``inventory`` Command instance.

        :returns: A new Command for ``provision inventory``.
    """
    @decorators.argument("spec_path")
    @decorators.option("--format", default="yaml")
    @decorators.command("inventory")
    def inventory_cmd(spec_path: str, format: str):
        _inventory_body(spec_path, format)
        return

    rtnval = inventory_cmd
    return rtnval


inventory_command = build_inventory_command()
