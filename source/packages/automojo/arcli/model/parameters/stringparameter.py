
from typing import List, Union


from automojo.arcli.model.parameters.parameterbase import ParameterBase


class StringParameter(ParameterBase[str]):

    def __init__(self, alias: str, tvalue: Union[str, List[str]]):
        super().__init__(alias, tvalue)
        return
    
    def get_value(self) -> str:
    
        cval = self._tvalue

        if cval.startswith('"') and cval.endswith('"'):
            cval = cval[1:-1]
        elif cval.startswith("'") and cval.endswith("'"):
            cval = cval[1:-1]

        return cval
