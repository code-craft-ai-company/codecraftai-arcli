
__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []

from typing import Optional

from ccai.arcli.model.parameters.stringparameter import StringParameter


class OptionalStringParameter(StringParameter):
    """
        Parameter type representing an optional string value.

        OptionalStringParameter is a variant of StringParameter. Since StringParameter
        already supports None values, this class exists primarily for semantic clarity
        and consistency with OptionalIntegerParameter.
    """

    def get_value(self) -> Optional[str]:

        if self._tvalue is None:
            return None

        return super().get_value()
