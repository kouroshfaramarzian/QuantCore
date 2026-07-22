import pandas as pd

from src.strategy.scoring import Scoring
from src.strategy.signals import Signal
from src.strategy.trend_filter import TrendFilter
from src.strategy.base_strategy import BaseStrategy

class SignalEngine(BaseStrategy):
    """
    Generates trading signals using scoring.
    """

    @staticmethod
    def generate(
        df: pd.DataFrame,
    ) -> dict:

        buy_score = Scoring.buy_score(df)
        sell_score = Scoring.sell_score(df)
        # -----------------------------
        # Trend Filter
        # -----------------------------

        if buy_score > sell_score:

            if not TrendFilter.allow_buy(df):

                buy_score = 0

        if sell_score > buy_score:

            if not TrendFilter.allow_sell(df):

                sell_score = 0
        if buy_score >= 70 and buy_score > sell_score:

            signal = Signal.BUY

        elif sell_score >= 70 and sell_score > buy_score:

            signal = Signal.SELL

        else:

            signal = Signal.HOLD

        return {
            "signal": signal,
            "buy_score": buy_score,
            "sell_score": sell_score,
        }