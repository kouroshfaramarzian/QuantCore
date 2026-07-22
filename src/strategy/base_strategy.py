from abc import ABC, abstractmethod

import pandas as pd


class BaseStrategy(ABC):
    """
    Base interface for every strategy.
    """

    @abstractmethod
    def generate(
        self,
        df: pd.DataFrame,
    ) -> dict:
        """
        Returns strategy decision.
        """
        pass