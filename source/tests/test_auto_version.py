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
import automojo

# create stub automojo.errors.exceptions module if not already mocked
if not hasattr(automojo, 'errors'):
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

from automojo.arcli import decorators

class TestAutoVersion(unittest.TestCase):

    def test_auto_version_flag(self):
        @decorators.entry(name="app", version="2.5.0")
        def main():
            """
            Main entry point.
            """
            pass

        sys.argv = ['app', '--version']
        buf = io.StringIO()
        with redirect_stdout(buf):
            with self.assertRaises(SystemExit) as cm:
                main()

        output = buf.getvalue().strip()
        self.assertEqual(cm.exception.code, 0)
        self.assertEqual(output, "2.5.0")

if __name__ == '__main__':
    unittest.main()
