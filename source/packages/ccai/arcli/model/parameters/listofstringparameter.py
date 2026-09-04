

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []

from typing import List, Union


from ccai.arcli.model.parameters.parameterbase import ParameterBase


class ListOfStringParameter(ParameterBase[List[str]]):

    def __init__(self, alias: str, tvalue: Union[str, List[str]]):
        super().__init__(alias, tvalue)
        return
    
    def get_value(self) -> List[str]:
    
        if self._tvalue is None:
            return []

        cval = []
        
        # Handle single string value
        if isinstance(self._tvalue, str):
            items_to_process = [self._tvalue]
        elif isinstance(self._tvalue, list):
            items_to_process = self._tvalue
        else:
            # Convert other types to list
            items_to_process = [str(self._tvalue)]

        for titem in items_to_process:
            if isinstance(titem, str):
                citem = titem
                # Only a value WRAPPED in matching quotes is unwrapped.  A
                # lone quote character satisfies startswith AND endswith on
                # its own, and [1:-1] would silently turn it into ''.
                if len(citem) >= 2 and citem[0] == citem[-1] and citem[0] in ('"', "'"):
                    citem = citem[1:-1]
            else:
                citem = str(titem)
            
            cval.append(citem)

        return cval
