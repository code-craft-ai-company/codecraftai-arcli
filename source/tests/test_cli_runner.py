
import sys
import unittest
import types
from pathlib import Path

# Ensure package paths
repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root / 'source/packages'))
sys.path.insert(0, str(repo_root)) # For examples

import automojo
from source.tests import setup_mocks

from automojo.arcli import CliRunner
import importlib

def load_example_command_entry():
    mod = importlib.import_module('source.examples.example_command')
    importlib.reload(mod)
    return mod.example_command_entry

class TestCliRunner(unittest.TestCase):

    def test_invoke_example_command(self):
        cmd = load_example_command_entry()
        runner = CliRunner()

        # Test basic invocation
        result = runner.invoke(cmd, args=['--some-a=foo'])

        self.assertEqual(result.exit_code, 0)
        output = result.stdout.strip().splitlines()
        # example_command prints: arg.some_a, arg.some_b, arg.some_optional
        # defaults: some_b="B", some_optional=None
        self.assertEqual(output, ['foo', 'B', 'None'])

    def test_invoke_with_string_args(self):
        cmd = load_example_command_entry()
        runner = CliRunner()

        # Test string args
        result = runner.invoke(cmd, args='--some-a=bar --some-b=baz')

        self.assertEqual(result.exit_code, 0)
        output = result.stdout.strip().splitlines()
        self.assertEqual(output, ['bar', 'baz', 'None'])

    def test_invoke_system_exit(self):
        # Create a mock callable that mimics EntryCommand signature but exits
        def mock_command(prog_name=None, args=None):
            print("Exiting...")
            sys.exit(42)

        runner = CliRunner()
        result = runner.invoke(mock_command, args=[])

        self.assertEqual(result.exit_code, 42)
        self.assertEqual(result.stdout.strip(), "Exiting...")
        self.assertIsNotNone(result.exception)
        self.assertIsInstance(result.exception, SystemExit)

    def test_invoke_exception(self):
        # Create a mock callable that raises an exception
        def mock_command(prog_name=None, args=None):
            raise ValueError("Something went wrong")

        runner = CliRunner()
        result = runner.invoke(mock_command, args=[])

        self.assertEqual(result.exit_code, 1)
        self.assertIsInstance(result.exception, ValueError)
        self.assertEqual(str(result.exception), "Something went wrong")

    def test_invoke_uncaught_exception(self):
         # Create a mock callable that raises an exception
        def mock_command(prog_name=None, args=None):
            raise ValueError("Something went wrong")

        runner = CliRunner()
        with self.assertRaises(ValueError):
            runner.invoke(mock_command, args=[], catch_exceptions=False)

if __name__ == '__main__':
    unittest.main()
