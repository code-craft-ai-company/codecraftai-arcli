import sys
import types
from pathlib import Path
import io
import unittest
from contextlib import redirect_stdout

# Ensure package paths
repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root / 'source/packages'))
sys.path.insert(0, str(repo_root))
import ccai

from source.tests import setup_mocks

from ccai.arcli import decorators

class TestAutoHelp(unittest.TestCase):

    def test_auto_help_generation(self):
        @decorators.argument("name", help="The name of the person to greet")
        @decorators.option("--greeting", default="Hello", help="The greeting to use")
        @decorators.command("greet")
        def greet_command(name, greeting):
            """
            Greets a person with a given greeting.
            """
            print(f"{greeting}, {name}!")

        @decorators.entry(name="app")
        def main():
            """
            Main entry point.
            """
            pass

        main.add_command(greet_command)

        # Test root help
        sys.argv = ['app', '--help']
        buf = io.StringIO()
        with redirect_stdout(buf):
            with self.assertRaises(SystemExit) as cm:
                main()

        output = buf.getvalue()
        self.assertEqual(cm.exception.code, 0)
        self.assertRegex(output, r"Usage: .* \[OPTIONS\] COMMAND \[ARGS\]\.\.\.")
        self.assertIn("Main entry point.", output)
        self.assertIn("greet  Greets a person with a given greeting.", output)

        # Test subcommand help
        sys.argv = ['app', 'greet', '--help']
        buf = io.StringIO()
        with redirect_stdout(buf):
            with self.assertRaises(SystemExit) as cm:
                main()

        output = buf.getvalue()
        self.assertEqual(cm.exception.code, 0)
        self.assertIn("Usage: greet [OPTIONS] NAME", output)
        self.assertIn("Greets a person with a given greeting.", output)
        self.assertIn("--greeting STRING", output)
        self.assertIn("The greeting to use", output)

if __name__ == '__main__':
    unittest.main()
