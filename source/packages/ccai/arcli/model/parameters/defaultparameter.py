

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []

from typing import Any, List, Union


from ccai.arcli.model.parameters.parameterbase import ParameterBase


class DefaultParameter(ParameterBase[Any]):

    def __init__(self, alias: str, tvalue: Union[Any, List[Any]]):
        super().__init__(alias, tvalue)
        return
    
    def get_value(self) -> Union[Any, None]:
        
        cval = self._tvalue

        return cval
