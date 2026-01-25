
import sys
import unittest
import types
from pathlib import Path
from typing import Optional

# Ensure package paths
repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root / 'source/packages'))
sys.path.insert(0, str(repo_root))

import automojo
from source.tests import setup_mocks

from automojo.arcli.model.parameters.optionalintegerparameter import OptionalIntegerParameter
from automojo.arcli.model.parameters.optionalstringparameter import OptionalStringParameter
from automojo.arcli.model.parameters.integerparameter import IntegerParameter
from automojo.arcli.model.parameters.stringparameter import StringParameter
from automojo.arcli.decorators import entry, option, command
from automojo.arcli import CliRunner

class TestOptionalParameters(unittest.TestCase):

    def test_optional_integer_parameter_none(self):
        param = OptionalIntegerParameter("test", None)
        self.assertIsNone(param.get_value())
        return

    def test_optional_integer_parameter_value(self):
        param = OptionalIntegerParameter("test", "123")
        self.assertEqual(param.get_value(), 123)
        return

    def test_integer_parameter_regression(self):
        # Verify IntegerParameter still returns 0 for None
        param = IntegerParameter("test", None)
        self.assertEqual(param.get_value(), 0)
        return

    def test_optional_string_parameter_none(self):
        param = OptionalStringParameter("test", None)
        self.assertIsNone(param.get_value())
        return

    def test_optional_string_parameter_value(self):
        param = OptionalStringParameter("test", "foo")
        self.assertEqual(param.get_value(), "foo")
        return

    def test_string_parameter_behavior(self):
        # Verify StringParameter returns None for None (as analyzed)
        param = StringParameter("test", None)
        self.assertIsNone(param.get_value())
        return

    def test_cli_usage(self):

        @option("--opt-int", ptype=OptionalIntegerParameter, default=None)
        @option("--opt-str", ptype=OptionalStringParameter, default=None)
        @entry()
        def my_command(opt_int: Optional[int], opt_str: Optional[str]):
            print(f"int: {opt_int}")
            print(f"str: {opt_str}")

        runner = CliRunner()

        # Test with defaults (None)
        result = runner.invoke(my_command, args=[])
        self.assertEqual(result.exit_code, 0)
        output = result.stdout.strip().splitlines()
        self.assertEqual(output[0], "int: None")
        self.assertEqual(output[1], "str: None")

        # Test with values
        result = runner.invoke(my_command, args=["--opt-int=42", "--opt-str=hello"])
        self.assertEqual(result.exit_code, 0)
        output = result.stdout.strip().splitlines()
        self.assertEqual(output[0], "int: 42")
        self.assertEqual(output[1], "str: hello")
        return

if __name__ == '__main__':
    unittest.main()
