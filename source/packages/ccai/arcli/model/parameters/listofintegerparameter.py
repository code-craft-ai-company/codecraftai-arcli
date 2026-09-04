

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []

from typing import List, Union


from ccai.arcli.model.parameters.parameterbase import ParameterBase


class ListOfIntegerParameter(ParameterBase[List[int]]):

    def __init__(self, alias: str, tvalue: Union[str, List[str]]):
        super().__init__(alias, tvalue)
        return
    
    def get_value(self) -> List[int]:
    
        if self._tvalue is None:
            return []

        cval = []
        
        # Handle single value
        if isinstance(self._tvalue, (str, int)):
            items_to_process = [self._tvalue]
        elif isinstance(self._tvalue, list):
            items_to_process = self._tvalue
        else:
            # Convert other types to list
            items_to_process = [self._tvalue]

        for titem in items_to_process:
            if isinstance(titem, str):
                citem = titem
                # Only a value WRAPPED in matching quotes is unwrapped.  A
                # lone quote character satisfies startswith AND endswith on
                # its own, and [1:-1] would silently turn it into ''.
                if len(citem) >= 2 and citem[0] == citem[-1] and citem[0] in ('"', "'"):
                    citem = citem[1:-1]
                
                try:
                    citem = int(citem)
                except ValueError:
                    errmsg = f"Error converting list item to integer value. item={titem}"
                    raise ValueError(errmsg)
            elif isinstance(titem, int):
                citem = titem
            else:
                try:
                    citem = int(titem)
                except (ValueError, TypeError):
                    errmsg = f"Error converting list item to integer value. item={titem}"
                    raise ValueError(errmsg)
            
            cval.append(citem)

        return cval
