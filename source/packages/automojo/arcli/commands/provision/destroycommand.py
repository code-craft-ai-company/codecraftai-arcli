"""
    .. module:: destroycommand
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: ``arcli provision destroy <spec.yaml>`` leaf command.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Automation Mojo LLC"
__credits__ = []


import sys

from automojo.arcli import decorators

from automojo.arcli.commands.common.aspectsfactory import (
    build_default_provisioning_aspects,
)
from automojo.arcli.commands.provision.enginefactory import build_engine
from automojo.arcli.commands.provision.specloader import load_provisioning_spec


def _confirm_destroy() -> bool:
    """
        Prompt for interactive destroy confirmation.

        :returns: True when the user types 'y' or 'yes'.
    """
    print("This will destroy resources described in the spec.")
    print("Are you sure? [y/N]: ", end="", flush=True)
    line = sys.stdin.readline()
    answer = line.strip().lower()

    confirmed = False
    if answer == "y" or answer == "yes":
        confirmed = True

    rtnval = confirmed
    return rtnval


def _destroy_body(spec_path: str, confirm: bool):
    """
        Loads the spec and drives ``ProvisioningEngine.destroy``.

        :param spec_path: Filesystem path to the spec YAML file.
        :param confirm: When True skip interactive confirmation.
    """
    try:
        spec = load_provisioning_spec(spec_path=spec_path)
    except FileNotFoundError as ferr:
        sys.stderr.write("{}\n".format(str(ferr)))
        sys.exit(2)
        return

    if confirm is not True:
        was_confirmed = _confirm_destroy()
        if was_confirmed is not True:
            print("No action taken.")
            return

    engine = build_engine(spec=spec)
    aspects = build_default_provisioning_aspects(confirm=True)
    engine.destroy(aspects=aspects)
    print("Destroy complete.")
    return


def build_destroy_command():
    """
        Build a fresh ``destroy`` Command instance.

        :returns: A new Command for ``provision destroy``.
    """
    @decorators.argument("spec_path")
    @decorators.option("--confirm/--no-confirm", alias="confirm", default=False)
    @decorators.command("destroy")
    def destroy_cmd(spec_path: str, confirm: bool):
        _destroy_body(spec_path, confirm)
        return

    rtnval = destroy_cmd
    return rtnval


destroy_command = build_destroy_command()
