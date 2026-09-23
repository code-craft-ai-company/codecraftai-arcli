
import sys
import unittest
from pathlib import Path
from typing import Optional

# Ensure package paths
repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root / 'source/packages'))
sys.path.insert(0, str(repo_root))

from source.tests import setup_mocks
setup_mocks.install_mocks()

from ccai.arcli.model.parameters.optionalbooleanparameter import OptionalBooleanParameter
from ccai.arcli.model.parameters.booleanparameter import BooleanParameter
from ccai.arcli.decorators import entry, option
from ccai.arcli import CliRunner

class TestOptionalBooleanParameter(unittest.TestCase):

    def test_optional_boolean_parameter_none(self):
        param = OptionalBooleanParameter("test", None)
        self.assertIsNone(param.get_value())
        return

    def test_optional_boolean_parameter_true(self):
        param = OptionalBooleanParameter("test", "true")
        self.assertTrue(param.get_value())
        return

    def test_optional_boolean_parameter_false(self):
        param = OptionalBooleanParameter("test", "false")
        self.assertFalse(param.get_value())
        return

    def test_boolean_parameter_regression(self):
        # Verify BooleanParameter still returns False for None
        param = BooleanParameter("test", None)
        self.assertFalse(param.get_value())
        return

    def test_cli_usage_default(self):
        @option("--opt-bool", ptype=OptionalBooleanParameter, default=None)
        @entry()
        def my_command(opt_bool: Optional[bool]):
            print(f"bool: {opt_bool}")

        runner = CliRunner()
        result = runner.invoke(my_command, args=[])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.stdout.strip(), "bool: None")
        return

    def test_cli_usage_true(self):
        @option("--opt-bool", ptype=OptionalBooleanParameter, default=None)
        @entry()
        def my_command(opt_bool: Optional[bool]):
            print(f"bool: {opt_bool}")

        runner = CliRunner()
        result = runner.invoke(my_command, args=["--opt-bool=true"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.stdout.strip(), "bool: True")
        return

    def test_cli_usage_false(self):
        @option("--opt-bool", ptype=OptionalBooleanParameter, default=None)
        @entry()
        def my_command(opt_bool: Optional[bool]):
            print(f"bool: {opt_bool}")

        runner = CliRunner()
        result = runner.invoke(my_command, args=["--opt-bool=false"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.stdout.strip(), "bool: False")
        return

if __name__ == '__main__':
    unittest.main()
