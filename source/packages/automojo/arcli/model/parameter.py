

from typing import Any, Union

from automojo.arcli.model.argfield import ArgField
from automojo.arcli.model.optionfield import OptionField


class Parameter:

    def __init__(self, field: Union[ArgField, OptionField], token: str):
        self._field = field
        self._token = token
        return
    
    @property
    def field(self) -> Union[ArgField, OptionField]:
        return self._field
    
    @property
    def token(self) -> str:
        return self._token
    
    def get_value(self) -> Any:
    
        # TODO: Implement parameter types and coversions
        return self._token
    
