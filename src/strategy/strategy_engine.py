import pandas as pd

from src.strategy.trend_engine import TrendEngine
from src.strategy.trigger_engine import TriggerEngine


class StrategyEngine:

    BUY = "BUY"

    SELL = "SELL"

    HOLD = "HOLD"

    @staticmethod
    def generate(
        df: pd.DataFrame,
    ) -> dict:

        trend = TrendEngine.detect(df)

        trigger = TriggerEngine.detect(df)

        signal = StrategyEngine.HOLD

        if (
            trend == TrendEngine.UPTREND
            and trigger == TriggerEngine.BUY
        ):

            signal = StrategyEngine.BUY

        elif (
            trend == TrendEngine.DOWNTREND
            and trigger == TriggerEngine.SELL
        ):

            signal = StrategyEngine.SELL

        return {

            "trend": trend,

            "trigger": trigger,

            "signal": signal,

        }