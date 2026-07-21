from typing import List

import pandas as pd

from src.backtest.trade import Trade


class Backtester:
    """
    Runs historical backtests.
    """

    def __init__(self):

        self.trades: List[Trade] = []

    def run(
        self,
        df: pd.DataFrame,
    ) -> List[Trade]:

        """
        Placeholder.

        Backtesting logic will be implemented
        in next step.
        """

        return self.trades