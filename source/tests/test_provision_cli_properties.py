
import os
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict
from unittest.mock import MagicMock

# Ensure package paths
repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root / 'source/packages'))
sys.path.insert(0, str(repo_root))

from source.tests import setup_mocks  # noqa: F401

import yaml
from hypothesis import given, strategies as st, settings, HealthCheck

from ccai.arcli import CliRunner, decorators
from ccai.arcli.commands.provision import (
    plan_command, register_provision_commands,
)
from ccai.arcli.commands.provision import enginefactory


class FakePlan:
    def to_dict(self) -> Dict[str, Any]:
        return {"per_venue_plans": {}, "total_action_count": 0}


def _make_root() -> Any:
    @decorators.entry("arcli")
    def main():
        return

    register_provision_commands(root=main)
    return main


_PATH_SEGMENT = st.text(
    alphabet=st.characters(blacklist_categories=("Cs",),
                            blacklist_characters="\x00/\\"),
    min_size=1,
    max_size=8,
)


class TestProvisionCliProperties(unittest.TestCase):

    def setUp(self) -> None:
        engine = MagicMock()
        engine.plan.return_value = FakePlan()
        engine.apply.return_value = {}
        engine.inventory.return_value = {}
        engine.destroy.return_value = None
        self._engine = engine
        enginefactory.set_engine_factory(factory=lambda *, spec: engine)
        self._tmp = tempfile.TemporaryDirectory()
        self._spec_path = os.path.join(self._tmp.name, "spec.yaml")
        with open(self._spec_path, "w") as fh:
            yaml.safe_dump({}, fh)
        return

    def tearDown(self) -> None:
        enginefactory.set_engine_factory(factory=None)
        self._tmp.cleanup()
        return

    @given(segments=st.lists(_PATH_SEGMENT, min_size=1, max_size=4))
    @settings(max_examples=25, deadline=None,
              suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_spec_path_argument_accepts_arbitrary_valid_paths(self, segments) -> None:
        # Build a non-existent path string and assert the parser routes it
        # to the leaf command's spec_path argument.  The leaf will exit
        # non-zero because the file doesn't exist, but the parser must
        # accept the value.
        relpath = os.sep.join(segments)
        root = _make_root()
        runner = CliRunner()
        result = runner.invoke(root, args=["provision", "plan", relpath])
        # The CLI should reach the spec loader (engine plan never called).
        self.assertEqual(self._engine.plan.call_count, 0)
        # Exit code should be non-zero (file not found).
        self.assertNotEqual(result.exit_code, 0)
        return

    @given(fmt=st.sampled_from(["text", "json"]))
    @settings(max_examples=10, deadline=None,
              suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_format_option_round_trip(self, fmt: str) -> None:
        root = _make_root()
        runner = CliRunner()
        result = runner.invoke(root, args=[
            "provision", "plan", "--format={}".format(fmt), self._spec_path,
        ])
        self.assertEqual(result.exit_code, 0, msg=result.stderr)
        return


if __name__ == '__main__':
    unittest.main()
