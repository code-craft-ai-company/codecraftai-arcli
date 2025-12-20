

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []

from typing import List, Union


from automojo.arcli.model.parameters.parameterbase import ParameterBase


class StringParameter(ParameterBase[str]):

    def __init__(self, alias: str, tvalue: Union[str, List[str]]):
        super().__init__(alias, tvalue)
        return
    
    def get_value(self) -> str:
        
        cval = self._tvalue

        if cval is not None:
            # Handle string values
            if isinstance(cval, str):
                if cval.startswith('"') and cval.endswith('"'):
                    cval = cval[1:-1]
                elif cval.startswith("'") and cval.endswith("'"):
                    cval = cval[1:-1]
            else:
                # Convert non-string values to string
                cval = str(cval)
        else:
            # Return empty string instead of None for consistency with type annotation
            cval = ""

        return cval
