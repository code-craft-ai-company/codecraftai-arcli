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
