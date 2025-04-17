
from typing import List, Union


from automojo.arcli.model.parameters.parameterbase import ParameterBase


class BooleanParameter(ParameterBase[bool]):

    def __init__(self, alias: str, tvalue: Union[str, List[str]]):
        super().__init__(alias, tvalue)
        return
    
    def get_value(self) -> bool:
    
        cval = self._tvalue

        if cval is not None:
            if cval.startswith('"') and cval.endswith('"'):
                cval = cval[1:-1]
            elif cval.startswith("'") and cval.endswith("'"):
                cval = cval[1:-1]

            cval = cval.lower()

            if cval in ["yes", "true"]:
                cval = True
            elif cval in ["no", "false"]:
                cval = False
            else:
                errmsg = f"Error converting command token to boolean value.  token={self._tvalue}"
                raise ValueError(errmsg)

        return cval
