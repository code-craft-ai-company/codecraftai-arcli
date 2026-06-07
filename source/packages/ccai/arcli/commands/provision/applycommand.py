"""
    .. module:: applycommand
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: ``arcli provision apply <spec.yaml>`` leaf command.

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
from ccai.arcli.commands.provision.renderers import render_plan, render_result
from ccai.arcli.commands.provision.specloader import load_provisioning_spec


def _confirm_apply(*, plan_text: str) -> bool:
    """
        Display the plan and prompt for interactive confirmation.

        :param plan_text: The rendered plan text.

        :returns: True when the user confirms, False otherwise.
    """
    print(plan_text)
    print("")
    print("Apply these changes? [y/N]: ", end="", flush=True)
    line = sys.stdin.readline()
    answer = line.strip().lower()

    confirmed = False
    if answer == "y" or answer == "yes":
        confirmed = True

    rtnval = confirmed
    return rtnval


def _apply_body(spec_path: str, format: str, confirm: bool, dry_run: bool):
    """
        Loads the spec and drives ``ProvisioningEngine.apply``.

        :param spec_path: Filesystem path to the spec YAML file.
        :param format: ``text`` or ``json``.
        :param confirm: When True skip interactive confirmation.
        :param dry_run: When True render the plan and exit.
    """
    try:
        spec = load_provisioning_spec(spec_path=spec_path)
    except FileNotFoundError as ferr:
        sys.stderr.write("{}\n".format(str(ferr)))
        sys.exit(2)

    engine = build_engine(spec=spec)

    if dry_run is True:
        aspects = build_default_provisioning_aspects(dry_run=True)
        plan = engine.plan(aspects=aspects)
        rendered = render_plan(plan=plan, fmt=format)
        print("[dry-run]")
        print(rendered)
        return

    plan_aspects = build_default_provisioning_aspects(dry_run=True)
    plan = engine.plan(aspects=plan_aspects)
    plan_text = render_plan(plan=plan, fmt="text")

    if confirm is not True:
        was_confirmed = _confirm_apply(plan_text=plan_text)
        if was_confirmed is not True:
            print("No action taken.")
            return

    apply_aspects = build_default_provisioning_aspects(dry_run=False)
    result = engine.apply(aspects=apply_aspects)
    rendered = render_result(result=result, fmt=format)
    print(rendered)
    return


def build_apply_command():
    """
        Build a fresh ``apply`` Command instance.

        :returns: A new Command for ``provision apply``.
    """
    @decorators.argument("spec_path")
    @decorators.option("--format", default="text")
    @decorators.option("--confirm/--no-confirm", alias="confirm", default=False)
    @decorators.option("--dry-run/--no-dry-run", alias="dry_run", default=False)
    @decorators.command("apply")
    def apply_cmd(spec_path: str, format: str, confirm: bool, dry_run: bool):
        _apply_body(spec_path, format, confirm, dry_run)
        return

    rtnval = apply_cmd
    return rtnval


apply_command = build_apply_command()
