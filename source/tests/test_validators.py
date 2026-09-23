
import sys
import unittest
from pathlib import Path

# Ensure package paths
# __file__ is source/tests/test_validators.py
# parents[0] is source/tests
# parents[1] is source
# parents[2] is root (.)
repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root / 'source/packages'))

sys.path.insert(0, str(repo_root))

from source.tests import setup_mocks
setup_mocks.install_mocks()

from ccai.errors.exceptions import SemanticError

from ccai.arcli.model.parameters.validators import Choice, Range, Path as PathParam, Regex, Custom
from ccai.arcli.model.parameters.integerparameter import IntegerParameter
from ccai.arcli.model.fields.optionfield import OptionMode
from ccai.arcli import CliRunner, decorators

class TestValidators(unittest.TestCase):

    def test_choice_validator(self):
        ChoiceType = Choice(['red', 'green', 'blue'])

        # Valid cases
        p = ChoiceType('color', 'red')
        self.assertEqual(p.get_value(), 'red')

        # Default is case sensitive, so Green should fail
        p = ChoiceType('color', 'Green')
        with self.assertRaises(ValueError):
            p.get_value()

        # Invalid cases
        p = ChoiceType('color', 'yellow')
        with self.assertRaises(ValueError):
            p.get_value()

        # Case insensitive
        ChoiceTypeCI = Choice(['red', 'green', 'blue'], case_sensitive=False)
        p = ChoiceTypeCI('color', 'Green')
        self.assertEqual(p.get_value(), 'green') # Returns value from choices

        # Non-string choices with IntegerParameter base
        ChoiceTypeInt = Choice([1, 2, 3], base_type=IntegerParameter)
        p = ChoiceTypeInt('num', '1')
        self.assertEqual(p.get_value(), 1)

    def test_range_validator(self):
        RangeType = Range(min_val=1, max_val=10)

        # Valid
        self.assertEqual(RangeType('num', '1').get_value(), 1)
        self.assertEqual(RangeType('num', '5').get_value(), 5)
        self.assertEqual(RangeType('num', '10').get_value(), 10)

        # Invalid
        with self.assertRaises(ValueError):
            RangeType('num', '0').get_value()

        with self.assertRaises(ValueError):
            RangeType('num', '11').get_value()

        # Optional parameter (None token)
        # Should return None, not 0 (which would fail range check 1-10)
        p = RangeType('num', None)
        self.assertIsNone(p.get_value())

    def test_path_validator(self):
        # We'll use this file as a guaranteed existing file
        current_file = str(Path(__file__).resolve())
        non_existent = str(Path(__file__).parent / "nonexistent.txt")

        PathType = PathParam(exists=True)

        self.assertEqual(PathType('path', current_file).get_value(), current_file)

        with self.assertRaises(ValueError):
            PathType('path', non_existent).get_value()

        # Test dir_okay/file_okay
        PathFileOnly = PathParam(exists=True, file_okay=True, dir_okay=False)
        self.assertEqual(PathFileOnly('path', current_file).get_value(), current_file)
        with self.assertRaises(ValueError):
             PathFileOnly('path', str(Path(__file__).parent)).get_value()

    def test_regex_validator(self):
        RegexType = Regex(r'^\d{3}-\d{2}-\d{4}$')

        self.assertEqual(RegexType('ssn', '123-45-6789').get_value(), '123-45-6789')

        with self.assertRaises(ValueError):
            RegexType('ssn', '123456789').get_value()

    def test_custom_validator(self):
        def my_converter(val):
            return val.upper()

        CustomType = Custom(my_converter)

        self.assertEqual(CustomType('custom', 'hello').get_value(), 'HELLO')

    def test_validator_error_is_reclassified_with_parameter_name(self):
        ChoiceType = Choice(["red", "green", "blue"])

        @decorators.option("--color", ptype=ChoiceType)
        @decorators.entry("app")
        def main(color):
            return

        runner = CliRunner()
        # SemanticError derives from BaseException on purpose: misuse must
        # halt the run, so CliRunner (which catches Exception only) does not
        # swallow it into a Result.  Assert the halt directly.
        with self.assertRaises(SemanticError) as caught:
            runner.invoke(main, args=["--color=orange"])
        self.assertIn("parameter 'color'", str(caught.exception))
        self.assertIn("Invalid value 'orange'", str(caught.exception))

    def test_optional_multiple_choice_without_value_does_not_raise(self):
        BreakpointType = Choice(["test-discovery", "testrun-start"])

        @decorators.option(
            "--breakpoint",
            alias="breakpoints",
            default=None,
            required=False,
            mode=OptionMode.Multiple,
            ptype=BreakpointType
        )
        @decorators.entry("app")
        def main(breakpoints):
            print(breakpoints)

        runner = CliRunner()
        result = runner.invoke(main, args=[])

        self.assertEqual(result.exit_code, 0)
        self.assertIsNone(result.exception)
        self.assertEqual(result.stdout.strip(), "None")

    def test_multiple_choice_validates_each_value(self):
        BreakpointType = Choice(["test-discovery", "testrun-start"])

        @decorators.option(
            "--breakpoint",
            alias="breakpoints",
            default=None,
            required=False,
            mode=OptionMode.Multiple,
            ptype=BreakpointType
        )
        @decorators.entry("app")
        def main(breakpoints):
            print(breakpoints)

        runner = CliRunner()
        result = runner.invoke(main, args=["--breakpoint=test-discovery", "--breakpoint=testrun-start"])

        self.assertEqual(result.exit_code, 0)
        self.assertIsNone(result.exception)
        self.assertEqual(result.stdout.strip(), "['test-discovery', 'testrun-start']")

    def test_multiple_range_validates_each_value(self):
        RangeType = Range(min_val=1, max_val=10)

        @decorators.option(
            "--count",
            alias="counts",
            default=None,
            required=False,
            mode=OptionMode.Multiple,
            ptype=RangeType
        )
        @decorators.entry("app")
        def main(counts):
            print(counts)

        runner = CliRunner()

        result_ok = runner.invoke(main, args=["--count=1", "--count=10"])
        self.assertEqual(result_ok.exit_code, 0)
        self.assertIsNone(result_ok.exception)
        self.assertEqual(result_ok.stdout.strip(), "[1, 10]")

        # SemanticError derives from BaseException on purpose: misuse must
        # halt the run, so CliRunner (which catches Exception only) does not
        # swallow it into a Result.  Assert the halt directly.
        with self.assertRaises(SemanticError) as caught:
            runner.invoke(main, args=["--count=11"])
        self.assertIn("parameter 'counts'", str(caught.exception))

    def test_multiple_path_validates_each_value(self):
        PathType = PathParam(exists=True, file_okay=True, dir_okay=False)

        @decorators.option(
            "--path",
            alias="paths",
            default=None,
            required=False,
            mode=OptionMode.Multiple,
            ptype=PathType
        )
        @decorators.entry("app")
        def main(paths):
            print(paths)

        runner = CliRunner()
        current_file = str(Path(__file__).resolve())

        result = runner.invoke(main, args=[f"--path={current_file}"])
        self.assertEqual(result.exit_code, 0)
        self.assertIsNone(result.exception)
        # The command prints the list's repr, which escapes backslashes on Windows.
        self.assertEqual(result.stdout.strip(), str([current_file]))

    def test_multiple_regex_validates_each_value(self):
        RegexType = Regex(r"^x+$")

        @decorators.option(
            "--token",
            alias="tokens",
            default=None,
            required=False,
            mode=OptionMode.Multiple,
            ptype=RegexType
        )
        @decorators.entry("app")
        def main(tokens):
            print(tokens)

        runner = CliRunner()

        result_ok = runner.invoke(main, args=["--token=x", "--token=xx"])
        self.assertEqual(result_ok.exit_code, 0)
        self.assertIsNone(result_ok.exception)
        self.assertEqual(result_ok.stdout.strip(), "['x', 'xx']")

        # SemanticError derives from BaseException on purpose: misuse must
        # halt the run, so CliRunner (which catches Exception only) does not
        # swallow it into a Result.  Assert the halt directly.
        with self.assertRaises(SemanticError) as caught:
            runner.invoke(main, args=["--token=y"])
        self.assertIn("parameter 'tokens'", str(caught.exception))

    def test_multiple_custom_converts_each_value(self):
        CustomType = Custom(lambda val: val.upper())

        @decorators.option(
            "--word",
            alias="words",
            default=None,
            required=False,
            mode=OptionMode.Multiple,
            ptype=CustomType
        )
        @decorators.entry("app")
        def main(words):
            print(words)

        runner = CliRunner()
        result = runner.invoke(main, args=["--word=foo", "--word=bar"])

        self.assertEqual(result.exit_code, 0)
        self.assertIsNone(result.exception)
        self.assertEqual(result.stdout.strip(), "['FOO', 'BAR']")

if __name__ == '__main__':
    unittest.main()
