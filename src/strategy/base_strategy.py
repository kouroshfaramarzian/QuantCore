from abc import ABC, abstractmethod

import pandas as pd


class BaseStrategy(ABC):
    """
    Base class for every strategy in QuantCore.

    Every strategy (Rule-Based, AI, Hybrid)
    must inherit from this class.
    """

    @abstractmethod
    def generate(
        self,
        df: pd.DataFrame,
    ) -> dict:
        """
        Generate trading signal.

        Returns
        -------
        dict

        Example

        {
            "signal": "BUY",
            "buy_score": 70,
            "sell_score": 15,
        }
        """

        raise NotImplementedError