import sys
import types
from pathlib import Path
import io
import unittest
from contextlib import redirect_stdout

# Ensure package paths
repo_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root / 'source/packages'))
sys.path.insert(0, str(repo_root))
import automojo

# create stub automojo.errors.exceptions module
err_mod = types.ModuleType('automojo.errors.exceptions')
class SemanticError(Exception):
    pass
class MissingOptionError(Exception):
    pass
class AbstractMethodError(Exception):
    pass
err_mod.SemanticError = SemanticError
err_mod.MissingOptionError = MissingOptionError
err_mod.AbstractMethodError = AbstractMethodError

errors_pkg = types.ModuleType('automojo.errors')
errors_pkg.exceptions = err_mod

automojo.errors = errors_pkg
sys.modules['automojo.errors'] = errors_pkg
sys.modules['automojo.errors.exceptions'] = err_mod

import importlib


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
        sys.argv = ['prog', '--some-a=A']
        buf = io.StringIO()
        with redirect_stdout(buf):
            cmd()
        self.assertEqual(buf.getvalue().strip().splitlines(), ['A', 'B', 'None'])


    def test_example_version_options(self):
        example_version = load_example_version_module()
        sys.argv = ['prog', '--some-a=A', '--some-b=B']
        buf = io.StringIO()
        with redirect_stdout(buf):
            example_version.example_command_entry()
        self.assertEqual(buf.getvalue().strip().splitlines(), ['A', 'B'])


    def test_example_version_trap(self):
        example_version = load_example_version_module()
        sys.argv = ['prog', '--some-a=A', '--some-b=B', '--version']
        buf = io.StringIO()
        with redirect_stdout(buf):
            with self.assertRaises(SystemExit) as cm:
                example_version.example_command_entry()
        self.assertEqual(cm.exception.code, 0)
        self.assertEqual(buf.getvalue().strip().splitlines(), ['1.0.0'])


if __name__ == '__main__':
    unittest.main()
