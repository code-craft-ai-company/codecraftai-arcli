
__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []

from typing import Optional

from ccai.arcli.model.parameters.booleanparameter import BooleanParameter


class OptionalBooleanParameter(BooleanParameter):
    """
        Parameter type representing an optional boolean value.

        OptionalBooleanParameter is a variant of BooleanParameter that allows the value
        to be None (i.e. not provided) instead of defaulting to False.
    """

    def get_value(self) -> Optional[bool]:

        if self._tvalue is None:
            return None

        return super().get_value()
