"""
    .. module:: specloader
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Helper for loading provisioning spec YAML files.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


import os

from typing import Any, Dict

import yaml


def load_provisioning_spec(*, spec_path: str) -> Dict[str, Any]:
    """
        Loads a provisioning spec from a YAML file.

        :param spec_path: Absolute or relative path to a YAML spec file.

        :returns: A parsed spec dictionary.
        :raises: FileNotFoundError, yaml.YAMLError
    """
    if not os.path.exists(spec_path):
        err_msg_lines = ["The provisioning spec file could not be found."]
        err_msg_lines.append("PATH: {}".format(spec_path))
        err_msg = os.linesep.join(err_msg_lines)
        raise FileNotFoundError(err_msg)

    with open(spec_path, "r") as fhandle:
        data = yaml.safe_load(fhandle)

    if data is None:
        data = {}

    rtnval = data
    return rtnval
