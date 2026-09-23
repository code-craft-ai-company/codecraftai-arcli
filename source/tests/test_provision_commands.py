
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

from source.tests import setup_mocks
setup_mocks.install_mocks()

import yaml

from ccai.arcli import CliRunner, decorators
from ccai.arcli.commands.provision import register_provision_commands
from ccai.arcli.commands.provision import enginefactory


SAMPLE_SPEC = {
    "venues": [
        {"name": "aws-lab", "kind": "aws"},
    ],
    "resources": [
        {"kind": "instance", "name": "node-a", "venue": "aws-lab"},
    ],
}


def _write_spec(*, tmpdir: str, payload: Dict[str, Any]) -> str:
    spec_path = os.path.join(tmpdir, "spec.yaml")
    with open(spec_path, "w") as fh:
        yaml.safe_dump(payload, fh)
    return spec_path


def _make_root() -> Any:
    @decorators.entry("arcli")
    def main():
        return

    register_provision_commands(root=main)
    return main


class FakePlan:
    def __init__(self) -> None:
        self._dict = {
            "per_venue_plans": {"aws-lab": {"actions": [{"kind": "instance"}]}},
            "topological_order": [["instance", "node-a"]],
            "total_action_count": 1,
        }

    def to_dict(self) -> Dict[str, Any]:
        return self._dict


class FakeResult:
    def to_dict(self) -> Dict[str, Any]:
        return {"created": ["node-a"], "updated": [], "skipped": [], "errors": []}


class FakeResource:
    def __init__(self, name: str, kind: str) -> None:
        self.name = name
        self.kind = kind

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "kind": self.kind}


def _build_fake_engine() -> MagicMock:
    engine = MagicMock()
    engine.plan.return_value = FakePlan()
    engine.apply.return_value = {"aws-lab": FakeResult()}
    engine.destroy.return_value = None
    engine.inventory.return_value = {"aws-lab": [FakeResource("node-a", "instance")]}
    return engine


class TestProvisionCommands(unittest.TestCase):

    def setUp(self) -> None:
        self._engine = _build_fake_engine()
        enginefactory.set_engine_factory(factory=lambda *, spec: self._engine)
        self._tmp = tempfile.TemporaryDirectory()
        self._spec_path = _write_spec(tmpdir=self._tmp.name, payload=SAMPLE_SPEC)
        return

    def tearDown(self) -> None:
        enginefactory.set_engine_factory(factory=None)
        self._tmp.cleanup()
        return

    # -- plan ----------------------------------------------------------------

    def test_plan_text_format_calls_engine(self) -> None:
        root = _make_root()
        runner = CliRunner()
        result = runner.invoke(root, args=["provision", "plan", self._spec_path])
        self.assertEqual(result.exit_code, 0, msg=result.stdout + result.stderr)
        self.assertEqual(self._engine.plan.call_count, 1)
        _, kwargs = self._engine.plan.call_args
        self.assertTrue(kwargs["aspects"].dry_run)
        self.assertIn("ProvisioningPlan", result.stdout)
        return

    def test_plan_json_format_emits_json(self) -> None:
        root = _make_root()
        runner = CliRunner()
        result = runner.invoke(root, args=["provision", "plan", "--format=json", self._spec_path])
        self.assertEqual(result.exit_code, 0, msg=result.stderr)
        import json
        parsed = json.loads(result.stdout.strip())
        self.assertEqual(parsed["total_action_count"], 1)
        return

    def test_plan_missing_file_exits_nonzero(self) -> None:
        root = _make_root()
        runner = CliRunner()
        result = runner.invoke(root, args=["provision", "plan", "/no/such/path.yaml"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertEqual(self._engine.plan.call_count, 0)
        return

    def test_plan_engine_exception_propagates(self) -> None:
        self._engine.plan.side_effect = RuntimeError("boom")
        root = _make_root()
        runner = CliRunner()
        result = runner.invoke(root, args=["provision", "plan", self._spec_path])
        self.assertEqual(result.exit_code, 1)
        self.assertIsInstance(result.exception, RuntimeError)
        return

    # -- apply ---------------------------------------------------------------

    def test_apply_with_confirm_calls_apply(self) -> None:
        root = _make_root()
        runner = CliRunner()
        result = runner.invoke(root, args=["provision", "apply", "--confirm", self._spec_path])
        self.assertEqual(result.exit_code, 0, msg=result.stderr)
        self.assertEqual(self._engine.apply.call_count, 1)
        self.assertIn("ProvisioningResult", result.stdout)
        return

    def test_apply_dry_run_skips_apply(self) -> None:
        root = _make_root()
        runner = CliRunner()
        result = runner.invoke(root, args=["provision", "apply", "--dry-run", self._spec_path])
        self.assertEqual(result.exit_code, 0, msg=result.stderr)
        self.assertEqual(self._engine.apply.call_count, 0)
        self.assertEqual(self._engine.plan.call_count, 1)
        self.assertIn("[dry-run]", result.stdout)
        return

    def test_apply_without_confirm_prompts_and_declines(self) -> None:
        import io as _io
        root = _make_root()
        runner = CliRunner()
        saved_stdin = sys.stdin
        sys.stdin = _io.StringIO("n\n")
        try:
            result = runner.invoke(root, args=["provision", "apply", self._spec_path])
        finally:
            sys.stdin = saved_stdin
        self.assertEqual(result.exit_code, 0, msg=result.stderr)
        self.assertIn("No action taken", result.stdout)
        self.assertEqual(self._engine.apply.call_count, 0)
        return

    def test_apply_without_confirm_prompts_and_accepts(self) -> None:
        import io as _io
        root = _make_root()
        runner = CliRunner()
        saved_stdin = sys.stdin
        sys.stdin = _io.StringIO("y\n")
        try:
            result = runner.invoke(root, args=["provision", "apply", self._spec_path])
        finally:
            sys.stdin = saved_stdin
        self.assertEqual(result.exit_code, 0, msg=result.stderr)
        self.assertEqual(self._engine.apply.call_count, 1)
        return

    # -- destroy -------------------------------------------------------------

    def test_destroy_with_confirm_calls_destroy(self) -> None:
        root = _make_root()
        runner = CliRunner()
        result = runner.invoke(root, args=["provision", "destroy", "--confirm", self._spec_path])
        self.assertEqual(result.exit_code, 0, msg=result.stderr)
        self.assertEqual(self._engine.destroy.call_count, 1)
        _, kwargs = self._engine.destroy.call_args
        self.assertTrue(kwargs["aspects"].confirm)
        return

    def test_destroy_without_confirm_declines(self) -> None:
        import io as _io
        root = _make_root()
        runner = CliRunner()
        saved_stdin = sys.stdin
        sys.stdin = _io.StringIO("n\n")
        try:
            result = runner.invoke(root, args=["provision", "destroy", self._spec_path])
        finally:
            sys.stdin = saved_stdin
        self.assertEqual(result.exit_code, 0)
        self.assertIn("No action taken", result.stdout)
        self.assertEqual(self._engine.destroy.call_count, 0)
        return

    # -- inventory -----------------------------------------------------------

    def test_inventory_yaml_format(self) -> None:
        root = _make_root()
        runner = CliRunner()
        result = runner.invoke(root, args=["provision", "inventory", self._spec_path])
        self.assertEqual(result.exit_code, 0, msg=result.stderr)
        self.assertEqual(self._engine.inventory.call_count, 1)
        parsed = yaml.safe_load(result.stdout)
        self.assertIn("aws-lab", parsed)
        self.assertEqual(parsed["aws-lab"][0]["name"], "node-a")
        return

    def test_inventory_json_format(self) -> None:
        root = _make_root()
        runner = CliRunner()
        result = runner.invoke(root, args=["provision", "inventory", "--format=json", self._spec_path])
        self.assertEqual(result.exit_code, 0, msg=result.stderr)
        import json
        parsed = json.loads(result.stdout.strip())
        self.assertIn("aws-lab", parsed)
        return


if __name__ == '__main__':
    unittest.main()
