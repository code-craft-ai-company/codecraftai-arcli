
import unittest
from unittest.mock import patch
import sys
from io import StringIO
from pathlib import Path

# Ensure package paths
repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root / 'source/packages'))
sys.path.insert(0, str(repo_root))

from source.tests import setup_mocks
setup_mocks.install_mocks()

from ccai.arcli.interact import InteractionStrategy, prompt_for_input, confirm, Spinner
from ccai.arcli.decorators import entry, option, argument
from ccai.arcli.errors import MissingOptionError
from ccai.arcli.model.fields.optionfield import OptionMode

class TestInteractionUtilities(unittest.TestCase):

    @patch('builtins.input', return_value='test_value')
    def test_prompt_for_input_returns_input(self, mock_input):
        result = prompt_for_input("Enter value")
        self.assertEqual(result, 'test_value')

    @patch('builtins.input', side_effect=['', 'retry_value'])
    def test_prompt_for_input_retries_on_empty_required(self, mock_input):
        # First input empty, second valid. required=True
        result = prompt_for_input("Enter value", required=True)
        self.assertEqual(result, 'retry_value')

    @patch('builtins.input', return_value='')
    def test_prompt_for_input_returns_default(self, mock_input):
        result = prompt_for_input("Enter value", default='default')
        self.assertEqual(result, 'default')

    @patch('builtins.input', return_value='y')
    def test_confirm_yes(self, mock_input):
        self.assertTrue(confirm("Are you sure?"))

    @patch('builtins.input', return_value='n')
    def test_confirm_no(self, mock_input):
        self.assertFalse(confirm("Are you sure?"))

    @patch('builtins.input', return_value='')
    def test_confirm_default(self, mock_input):
        self.assertFalse(confirm("Are you sure?", default=False))
        self.assertTrue(confirm("Are you sure?", default=True))

class TestSpinner(unittest.TestCase):
    def test_spinner_context_manager(self):
        # Just ensure it doesn't crash, harder to test visual output
        with Spinner("Loading..."):
            pass

class TestInteractionIntegration(unittest.TestCase):

    def test_entry_command_with_interaction_strategy(self):
        @entry(interaction_strategy=InteractionStrategy.ALLOW)
        def my_cmd(context):
            pass

        self.assertEqual(my_cmd._context.interaction_strategy, InteractionStrategy.ALLOW)

    @patch('ccai.arcli.parsing.prompt_for_input', return_value='interactive_val')
    def test_missing_required_option_prompts_when_allowed(self, mock_prompt):

        @option('--req', required=True)
        @entry(interaction_strategy=InteractionStrategy.ALLOW)
        def my_cmd(req):
            print(f"Got {req}")

        # Simulate empty args
        args = []
        # We need to manually invoke the parser logic usually done in EntryCommand.__call__
        # But EntryCommand.__call__ calls self._command_entry which does the parsing.

        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            my_cmd(args=args)
        except SystemExit:
            # Expected: the CLI entry point may end with sys.exit(); the prompt and output are verified below.
            pass
        finally:
            sys.stdout = sys.__stdout__

        mock_prompt.assert_called()
        self.assertIn("Got interactive_val", captured_output.getvalue())

    def test_missing_required_option_raises_when_never(self):
        @option('--req', required=True)
        @entry(interaction_strategy=InteractionStrategy.NEVER)
        def my_cmd(req):
            pass

        try:
            my_cmd(args=[])
            self.fail("MissingOptionError not raised")
        except MissingOptionError:
            # Expected: with InteractionStrategy.NEVER a missing required option must raise instead of prompting.
            pass
        except Exception as e:
            self.fail(f"Raised wrong exception: {e}")

    @patch('ccai.arcli.parsing.prompt_for_input', return_value='interactive_arg')
    def test_missing_required_argument_prompts_when_allowed(self, mock_prompt):
        @argument('myarg', required=True)
        @entry(interaction_strategy=InteractionStrategy.ALLOW)
        def my_cmd(myarg):
            print(f"Got {myarg}")

        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            my_cmd(args=[])
        except Exception as e:
            # If it failed for another reason, we want to know
            print(e)
        finally:
            sys.stdout = sys.__stdout__

        mock_prompt.assert_called()
        self.assertIn("Got interactive_arg", captured_output.getvalue())

    @patch('ccai.arcli.parsing.prompt_for_input', return_value='interactive_multi')
    def test_missing_required_multiple_option_prompts_when_allowed(self, mock_prompt):
        @option('--req', required=True, mode=OptionMode.Multiple)
        @entry(interaction_strategy=InteractionStrategy.ALLOW)
        def my_cmd(req):
            print(f"Got {req}")

        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            my_cmd(args=[])
        except SystemExit:
            # Expected: the CLI entry point may end with sys.exit(); the prompt and output are verified below.
            pass
        finally:
            sys.stdout = sys.__stdout__

        mock_prompt.assert_called()
        self.assertIn("Got ['interactive_multi']", captured_output.getvalue())

    @patch('ccai.arcli.parsing.prompt_for_input', return_value='interactive_counter')
    def test_missing_required_counter_option_prompts_when_allowed(self, mock_prompt):
        @option('--req', required=True, mode=OptionMode.Counter)
        @entry(interaction_strategy=InteractionStrategy.ALLOW)
        def my_cmd(req):
            print(f"Got {req}")

        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            my_cmd(args=[])
        except SystemExit:
            # Expected: the CLI entry point may end with sys.exit(); the prompt and output are verified below.
            pass
        finally:
            sys.stdout = sys.__stdout__

        mock_prompt.assert_called()
        self.assertIn("Got 1", captured_output.getvalue())

if __name__ == '__main__':
    unittest.main()
