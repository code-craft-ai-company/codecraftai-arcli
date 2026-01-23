

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []

import sys

from automojo.arcli.interact import InteractionStrategy

class CliContext:
    """
    """

    def __init__(self, interaction_strategy: InteractionStrategy = InteractionStrategy.NEVER):
        self._interaction_strategy = interaction_strategy
        return

    @property
    def interaction_strategy(self) -> InteractionStrategy:
        return self._interaction_strategy

    