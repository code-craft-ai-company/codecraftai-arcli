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

from ccai.arcli import decorators

class TestTraps(unittest.TestCase):

    def test_trap_callback(self):

        trap_triggered = False

        def my_trap():
            nonlocal trap_triggered
            trap_triggered = True
            pass

        @decorators.trap("--my-trap", trap_callback=my_trap)
        @decorators.entry()
        def main():
            print("main executed")

        sys.argv = ['app', '--my-trap']
        buf = io.StringIO()
        with redirect_stdout(buf):
            try:
                main()
            except SystemExit:
                pass

        output = buf.getvalue().strip()
        self.assertTrue(trap_triggered, "Trap callback should be called")
        self.assertNotIn("main executed", output, "Main command should not execute if trap is triggered")

    def test_multiple_traps(self):

        trap_a_triggered = False
        trap_b_triggered = False

        def trap_a():
            nonlocal trap_a_triggered
            trap_a_triggered = True

        def trap_b():
            nonlocal trap_b_triggered
            trap_b_triggered = True

        @decorators.trap("--trap-a", trap_callback=trap_a)
        @decorators.trap("--trap-b", trap_callback=trap_b)
        @decorators.entry()
        def main():
            pass

        # If multiple traps are provided, which one runs? Or both?
        # Usually first one encountered or priority?
        # Let's try triggering A.
        sys.argv = ['app', '--trap-a']
        try:
            main()
        except SystemExit:
            pass
        self.assertTrue(trap_a_triggered)
        self.assertFalse(trap_b_triggered)

if __name__ == '__main__':
    unittest.main()
