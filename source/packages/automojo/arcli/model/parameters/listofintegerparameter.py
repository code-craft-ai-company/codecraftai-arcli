

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []

from typing import List, Union


from automojo.arcli.model.parameters.parameterbase import ParameterBase


class ListOfStringParameter(ParameterBase[List[int]]):

    def __init__(self, alias: str, tvalue: Union[str, List[str]]):
        super().__init__(alias, tvalue)
        return
    
    def get_value(self) -> List[int]:
    
        cval = None

        if self._tvalue is not None:
            cval = []

            for titem in self._tvalue:

                citem = titem

                if citem.startswith('"') and citem.endswith('"'):
                    citem = citem[1:-1]
                elif citem.startswith("'") and citem.endswith("'"):
                    citem = citem[1:-1]

                citem = int(citem)

                cval.append(citem)

        return cval
