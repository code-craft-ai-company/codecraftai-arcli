"""
    .. module:: plancommand
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: ``arcli provision plan <spec.yaml>`` leaf command.

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
from ccai.arcli.commands.provision.renderers import render_plan
from ccai.arcli.commands.provision.specloader import load_provisioning_spec


def _plan_body(spec_path: str, format: str):
    """
        Loads the spec, drives ``ProvisioningEngine.plan`` with dry-run aspects,
        and renders the returned plan.

        :param spec_path: Filesystem path to the spec YAML file.
        :param format: ``text`` or ``json``.
    """
    try:
        spec = load_provisioning_spec(spec_path=spec_path)
    except FileNotFoundError as ferr:
        sys.stderr.write("{}\n".format(str(ferr)))
        sys.exit(2)

    aspects = build_default_provisioning_aspects(dry_run=True)
    engine = build_engine(spec=spec)
    plan = engine.plan(aspects=aspects)

    rendered = render_plan(plan=plan, fmt=format)
    print(rendered)
    return


def build_plan_command():
    """
        Build a fresh ``plan`` Command instance.  Always construct a new
        instance to avoid shared OptionField/ArgField token state between
        invocations.

        :returns: A new Command for ``provision plan``.
    """
    @decorators.argument("spec_path")
    @decorators.option("--format", default="text")
    @decorators.command("plan")
    def plan_cmd(spec_path: str, format: str):
        _plan_body(spec_path, format)
        return

    rtnval = plan_cmd
    return rtnval


plan_command = build_plan_command()
