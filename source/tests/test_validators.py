
import sys
import unittest
import os
from pathlib import Path
import types

# Ensure package paths
# __file__ is source/tests/test_validators.py
# parents[0] is source/tests
# parents[1] is source
# parents[2] is root (.)
repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root / 'source/packages'))

sys.path.insert(0, str(repo_root))

import automojo
from source.tests import setup_mocks

from automojo.arcli.model.parameters.validators import Choice, Range, Path as PathParam, Regex, Custom
from automojo.arcli.model.parameters.parameterbase import ParameterBase
from automojo.arcli.model.parameters.integerparameter import IntegerParameter

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

if __name__ == '__main__':
    unittest.main()
