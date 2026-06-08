
__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []

from typing import Union, Optional

from ccai.arcli.model.parameters.integerparameter import IntegerParameter


class OptionalIntegerParameter(IntegerParameter):
    """
        Parameter type representing an optional integer value.

        OptionalIntegerParameter is a variant of IntegerParameter that allows the value
        to be None (i.e. not provided) instead of defaulting to 0.
    """

    def get_value(self) -> Optional[int]:

        if self._tvalue is None:
            return None

        return super().get_value()
