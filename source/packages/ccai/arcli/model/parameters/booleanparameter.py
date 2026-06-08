

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []

from typing import List, Union


from ccai.arcli.model.parameters.parameterbase import ParameterBase


class BooleanParameter(ParameterBase[bool]):

    def __init__(self, alias: str, tvalue: Union[str, List[str]]):
        super().__init__(alias, tvalue)
        return
    
    def get_value(self) -> bool:
    
        cval = self._tvalue

        if cval is not None:
            # If it's already a boolean, return it directly
            if isinstance(cval, bool):
                return cval
            
            # Handle string values
            if isinstance(cval, str):
                if cval.startswith('"') and cval.endswith('"'):
                    cval = cval[1:-1]
                elif cval.startswith("'") and cval.endswith("'"):
                    cval = cval[1:-1]

                cval = cval.lower()

                if cval in ["yes", "true", "1"]:
                    cval = True
                elif cval in ["no", "false", "0"]:
                    cval = False
                else:
                    errmsg = f"Error converting command token to boolean value.  token={self._tvalue}"
                    raise ValueError(errmsg)
            else:
                errmsg = f"Invalid type for boolean parameter: {type(cval)}"
                raise ValueError(errmsg)
        else:
            # Default to False when no value is provided
            cval = False

        return cval
