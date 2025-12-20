

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []

from typing import List, Union

from automojo.arcli.model.parameters.parameterbase import ParameterBase


class IntegerParameter(ParameterBase[int]):

    def __init__(self, alias: str, tvalue: Union[str, List[str]]):
        super().__init__(alias, tvalue)
        return
    
    def get_value(self) -> int:
    
        cval = self._tvalue

        if cval is not None:
            # Handle string values that need parsing
            if isinstance(cval, str):
                if cval.startswith('"') and cval.endswith('"'):
                    cval = cval[1:-1]
                elif cval.startswith("'") and cval.endswith("'"):
                    cval = cval[1:-1]
                
                try:
                    cval = int(cval)
                except ValueError:
                    errmsg = f"Error converting command token to integer value. token={self._tvalue}"
                    raise ValueError(errmsg)
            elif isinstance(cval, int):
                # Already an integer, use as-is
                pass
            else:
                # Try to convert other types to int
                try:
                    cval = int(cval)
                except (ValueError, TypeError):
                    errmsg = f"Error converting command token to integer value. token={self._tvalue}"
                    raise ValueError(errmsg)
        else:
            # Return 0 instead of None for consistency with type annotation
            cval = 0

        return cval
