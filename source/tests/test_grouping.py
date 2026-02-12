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
from automojo.errors.exceptions import SemanticError

from automojo.arcli import decorators
from automojo.arcli.model.groupingcommand import GroupingCommand

class TestGrouping(unittest.TestCase):

    def test_nested_commands(self):

        @decorators.command("sub")
        def sub_command():
            print("sub executed")

        @decorators.group("grp")
        def group_command():
            print("group executed")

        @decorators.entry("app")
        def main():
            print("main executed")

        group_command.add_command(sub_command)
        main.add_command(group_command)

        # Execute: app grp sub
        sys.argv = ['app', 'grp', 'sub']
        buf = io.StringIO()
        with redirect_stdout(buf):
            try:
                main()
            except SystemExit:
                pass

        output = buf.getvalue().strip()
        self.assertIn("main executed", output)
        self.assertIn("group executed", output)
        self.assertIn("sub executed", output)

    def test_group_has_children(self):
        @decorators.group("grp")
        def group_command():
            pass

        @decorators.command("sub")
        def sub_command():
            pass

        self.assertFalse(group_command.has_children)
        group_command.add_command(sub_command)
        self.assertTrue(group_command.has_children)
        self.assertTrue(group_command.has_child_command("sub"))
        self.assertFalse(group_command.has_child_command("other"))

    def test_add_invalid_command(self):
        @decorators.group("grp")
        def group_command():
            pass

        def not_a_command():
            pass

        with self.assertRaises(SemanticError):
            group_command.add_command(not_a_command)

    def test_child_command_state_is_reset_between_invocations(self):
        @decorators.command("sub")
        def sub_command():
            print("sub executed")

        @decorators.entry("app")
        def main():
            print("main executed")

        main.add_command(sub_command)

        first_buffer = io.StringIO()
        with redirect_stdout(first_buffer):
            main(args=["sub"])

        first_output = first_buffer.getvalue().strip().splitlines()
        self.assertEqual(first_output, ["main executed", "sub executed"])

        second_buffer = io.StringIO()
        with redirect_stdout(second_buffer):
            main(args=[])

        second_output = second_buffer.getvalue().strip().splitlines()
        self.assertEqual(second_output, ["main executed"])

    def test_unknown_equals_option_raises_semantic_error(self):
        @decorators.option("--known")
        @decorators.entry("app")
        def main(known):
            pass

        with self.assertRaises(SemanticError):
            main(args=["--unknown=1"])

    def test_option_without_flags_raises_semantic_error(self):
        with self.assertRaises(SemanticError):
            @decorators.option()
            @decorators.entry("app")
            def main():
                pass

    def test_trap_without_flags_raises_semantic_error(self):
        with self.assertRaises(SemanticError):
            @decorators.trap(trap_callback=lambda: None)
            @decorators.entry("app")
            def main():
                pass

if __name__ == '__main__':
    unittest.main()
