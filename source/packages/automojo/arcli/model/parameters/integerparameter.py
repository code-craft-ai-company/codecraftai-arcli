
from typing import List, Union

from automojo.arcli.model.parameters.parameterbase import ParameterBase


class IntegerParameter(ParameterBase[int]):

    def __init__(self, alias: str, tvalue: Union[str, List[str]]):
        super().__init__(alias, tvalue)
        return
    
    def get_value(self) -> str:
    
        cval = self._tvalue

        if cval is not None:
            if cval.startswith('"') and cval.endswith('"'):
                cval = cval[1:-1]
            elif cval.startswith("'") and cval.endswith("'"):
                cval = cval[1:-1]
            
            cval = int(cval)

        return cval
