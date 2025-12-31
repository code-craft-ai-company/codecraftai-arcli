
__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []

from typing import Generic, List, TypeVar, Union

from automojo.errors.exceptions import AbstractMethodError


PT = TypeVar("PT")

class ParameterBase(Generic[PT]):

    def __init__(self, alias: str, tvalue: Union[str, List[str]]):
        self._alias = alias
        self._tvalue = tvalue
        return
    
    @property
    def alias(self) -> str:
        return self._alias

    @property
    def tvalue(self) -> str:
        return self._tvalue
    
    def get_value(self) -> Union[PT, None]:
        """
            An abstract method that must be overridden by derived 'Parameter' types.  This method is called in order to convert
            tokens from the command-line into a value of a given type.
        """
        errmsg = "The 'get_value' method must be overridden by derived parameter types."
        raise AbstractMethodError(errmsg)
