import sys
import unittest
from pathlib import Path
import io
from contextlib import redirect_stdout

# Ensure package paths
repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root / 'source/packages'))
sys.path.insert(0, str(repo_root))

from source.tests import setup_mocks
setup_mocks.install_mocks()
from ccai.errors.exceptions import SemanticError

from ccai.arcli.model.optiongroup import OptionGroup
from ccai.arcli.model.fields.optionfield import OptionField
from ccai.arcli import decorators

class MyOptions(OptionGroup):
    name = "My Options"

    opt_a = OptionField("--opt-a", help="Option A {extra}")
    opt_b = OptionField("--opt-b", default="B", help="Option B")

class TestOptionGroups(unittest.TestCase):

    def test_option_group_attach(self):

        @MyOptions.attach(help_fill={"extra": ""})
        @decorators.entry()
        def main(opt_a, opt_b):
            print(f"opt_a={opt_a}, opt_b={opt_b}")

        # Test execution
        sys.argv = ['app', '--opt-a=foo']
        buf = io.StringIO()
        with redirect_stdout(buf):
            try:
                main()
            except SystemExit:
                # Expected: the CLI entry point ends with sys.exit(); the captured output is verified below.
                pass

        output = buf.getvalue().strip()
        self.assertEqual(output, "opt_a=foo, opt_b=B")

    def test_option_group_help_fill(self):

        @MyOptions.attach(help_fill={"extra": "with icing"})
        @decorators.entry()
        def main(opt_a, opt_b):
            pass

        # Verify help text was updated
        # We need to inspect the command object
        # The main function is an EntryCommand instance

        # Find the option field for opt_a
        opt_a_field = main.lookup_field_by_alias("opt_a")
        self.assertIsNotNone(opt_a_field)
        self.assertEqual(opt_a_field.help, "Option A with icing")

        opt_b_field = main.lookup_field_by_alias("opt_b")
        self.assertEqual(opt_b_field.help, "Option B")

    def test_option_group_validation(self):
        # Test that empty name raises SemanticError
        with self.assertRaises(SemanticError):
            class BadOptions(OptionGroup):
                name = ""
            BadOptions()

    def test_option_group_validation_no_name(self):
        # Test that no name raises SemanticError (it defaults to "" in base class)
        with self.assertRaises(SemanticError):
            class BadOptionsNoName(OptionGroup):
                pass
            BadOptionsNoName()

if __name__ == '__main__':
    unittest.main()
