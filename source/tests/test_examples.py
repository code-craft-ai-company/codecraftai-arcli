import sys
import types
from pathlib import Path
import unittest

# Ensure package paths
repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root / 'source/packages'))
sys.path.insert(0, str(repo_root))
import automojo

from source.tests import setup_mocks

import importlib
from automojo.arcli import CliRunner

def load_example_command_entry():
    mod = importlib.import_module('source.examples.example_command')
    importlib.reload(mod)
    return mod.example_command_entry


def load_example_version_module():
    mod = importlib.import_module('source.examples.example_version')
    importlib.reload(mod)
    return mod


class TestExamples(unittest.TestCase):

    def test_example_command_defaults(self):
        cmd = load_example_command_entry()
        runner = CliRunner()
        result = runner.invoke(cmd, args=['--some-a=A'], prog_name='prog')
        self.assertEqual(result.output.strip().splitlines(), ['A', 'B', 'None'])


    def test_example_version_options(self):
        example_version = load_example_version_module()
        runner = CliRunner()
        result = runner.invoke(example_version.example_command_entry, args=['--some-a=A', '--some-b=B'], prog_name='prog')
        self.assertEqual(result.output.strip().splitlines(), ['A', 'B'])


    def test_example_version_trap(self):
        example_version = load_example_version_module()
        runner = CliRunner()
        result = runner.invoke(example_version.example_command_entry, args=['--some-a=A', '--some-b=B', '--version'], prog_name='prog')
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.strip().splitlines(), ['1.0.0'])


if __name__ == '__main__':
    unittest.main()
