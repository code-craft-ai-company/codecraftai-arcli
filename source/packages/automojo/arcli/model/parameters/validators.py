
__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []

import os
import re
from typing import Any, Callable, List, Optional, Type, Union

from automojo.arcli.model.parameters.parameterbase import ParameterBase
from automojo.arcli.model.parameters.stringparameter import StringParameter
from automojo.arcli.model.parameters.integerparameter import IntegerParameter

def Choice(choices: List[Any], case_sensitive: bool = True, base_type: Type[ParameterBase] = StringParameter) -> Type[ParameterBase]:
    """
    Factory that returns a parameter type for restricting input to a set of valid values.
    """
    class ChoiceParameter(base_type):
        _choices = choices
        _case_sensitive = case_sensitive

        def _validate_choice_value(self, val: Any) -> Any:
            check_val = val
            valid_choices = self._choices

            if not self._case_sensitive:
                check_val = str(check_val).lower()
                valid_choices = [str(c).lower() for c in self._choices]

            if check_val not in valid_choices:
                errmsg = f"Invalid value '{val}'. Allowed values are: {', '.join(map(str, self._choices))}"
                raise ValueError(errmsg)

            if not self._case_sensitive:
                idx = valid_choices.index(check_val)
                return self._choices[idx]

            return val

        def get_value(self) -> Any:
            if isinstance(self._tvalue, list):
                validated_values = []
                for titem in self._tvalue:
                    citem = base_type(self._alias, titem).get_value()
                    vitem = self._validate_choice_value(citem)
                    validated_values.append(vitem)

                return validated_values

            val = super().get_value()
            if val is None:
                return None

            val = self._validate_choice_value(val)

            return val

    return ChoiceParameter


def Range(min_val: Optional[Union[int, float]] = None, max_val: Optional[Union[int, float]] = None) -> Type[ParameterBase]:
    """
    Factory that returns a parameter type for ensuring numbers are within a specific range.
    Defaults to IntegerParameter behavior for parsing, but validates range.
    """
    class RangeParameter(IntegerParameter):
        _min = min_val
        _max = max_val

        def _validate_range_value(self, val: int) -> int:
            if self._min is not None and val < self._min:
                raise ValueError(f"Value {val} is smaller than the minimum allowed value {self._min}")

            if self._max is not None and val > self._max:
                raise ValueError(f"Value {val} is larger than the maximum allowed value {self._max}")

            return val

        def get_value(self) -> Union[int, List[int], None]:
            if isinstance(self._tvalue, list):
                validated_values = []
                for titem in self._tvalue:
                    citem = IntegerParameter(self._alias, titem).get_value()
                    vitem = self._validate_range_value(citem)
                    validated_values.append(vitem)

                return validated_values

            # Check if value is present before validation
            # IntegerParameter returns 0 for None, which might cause range validation failure
            if self._tvalue is None:
                return None

            val = super().get_value()

            val = self._validate_range_value(val)

            return val

    return RangeParameter


def Path(exists: bool = False, file_okay: bool = True, dir_okay: bool = True,
         writable: bool = False, readable: bool = True, resolve_path: bool = False) -> Type[ParameterBase]:
    """
    Factory that returns a parameter type for validating file system paths.
    """
    class PathParameter(StringParameter):
        def _validate_path_value(self, val: str) -> str:
            if resolve_path:
                val = os.path.abspath(val)

            if exists:
                if not os.path.exists(val):
                    raise ValueError(f"Path '{val}' does not exist.")

                if file_okay and not dir_okay:
                    if not os.path.isfile(val):
                        raise ValueError(f"Path '{val}' is not a file.")

                if dir_okay and not file_okay:
                    if not os.path.isdir(val):
                        raise ValueError(f"Path '{val}' is not a directory.")

                if readable and not os.access(val, os.R_OK):
                     raise ValueError(f"Path '{val}' is not readable.")

                if writable and not os.access(val, os.W_OK):
                     raise ValueError(f"Path '{val}' is not writable.")

            return val
        
        def get_value(self) -> Union[str, List[str], None]:
            if isinstance(self._tvalue, list):
                validated_values = []
                for titem in self._tvalue:
                    citem = StringParameter(self._alias, titem).get_value()
                    vitem = self._validate_path_value(citem)
                    validated_values.append(vitem)

                return validated_values

            val = super().get_value()
            if val is None:
                return None

            val = self._validate_path_value(val)

            return val

    return PathParameter


def Regex(pattern: str, flags: int = 0) -> Type[ParameterBase]:
    """
    Factory that returns a parameter type for validating input against a regular expression.
    """
    class RegexParameter(StringParameter):
        _pattern = re.compile(pattern, flags)

        def _validate_regex_value(self, val: str) -> str:
            if not self._pattern.match(val):
                raise ValueError(f"Value '{val}' does not match pattern '{pattern}'")

            return val
        
        def get_value(self) -> Union[str, List[str], None]:
            if isinstance(self._tvalue, list):
                validated_values = []
                for titem in self._tvalue:
                    citem = StringParameter(self._alias, titem).get_value()
                    vitem = self._validate_regex_value(citem)
                    validated_values.append(vitem)

                return validated_values

            val = super().get_value()
            if val is None:
                return None

            val = self._validate_regex_value(val)

            return val

    return RegexParameter


def Custom(converter: Callable[[str], Any]) -> Type[ParameterBase]:
    """
    Factory that creates a parameter type with custom parsing logic.
    """
    class CustomParameter(ParameterBase):
        def _normalize_value(self, val: Any) -> Any:
            if isinstance(val, str):
                if val.startswith('"') and val.endswith('"'):
                    val = val[1:-1]
                elif val.startswith("'") and val.endswith("'"):
                    val = val[1:-1]

            return val

        def get_value(self) -> Any:
            val = self._tvalue
            if val is None:
                return None

            if isinstance(val, list):
                converted_values = []
                for titem in val:
                    citem = self._normalize_value(titem)
                    cvitem = converter(citem)
                    converted_values.append(cvitem)

                return converted_values

            val = self._normalize_value(val)

            return converter(val)

    return CustomParameter
