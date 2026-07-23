import pandas as pd

from src.features.trend import TrendIndicators
from src.features.momentum import MomentumIndicators
from src.features.volatility import VolatilityIndicators
from src.features.candles import CandleFeatures
from src.price_action.structure import MarketStructure

class FeatureEngine:
    """
    Creates all technical features.
    """

    @staticmethod
    def transform(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df = df.copy()

        # Trend
        df["EMA20"] = TrendIndicators.ema(df, 20)
        df["EMA50"] = TrendIndicators.ema(df, 50)
        df["EMA200"] = TrendIndicators.ema(df, 200)

        macd, signal, hist = TrendIndicators.macd(df)

        df["MACD"] = macd
        df["MACD_SIGNAL"] = signal
        df["MACD_HIST"] = hist

        # Momentum
        df["RSI14"] = MomentumIndicators.rsi(df)

        # Volatility
        df["ATR14"] = VolatilityIndicators.atr(df)

        upper, middle, lower = (
            VolatilityIndicators.bollinger(df)
        )

        df["BB_UPPER"] = upper
        df["BB_MIDDLE"] = middle
        df["BB_LOWER"] = lower
                # Candle Features
        df["BODY"] = CandleFeatures.body(df)

        df["UPPER_WICK"] = (
            CandleFeatures.upper_wick(df)
        )

        df["LOWER_WICK"] = (
            CandleFeatures.lower_wick(df)
        )

        df["RANGE"] = (
            CandleFeatures.candle_range(df)
        )

        df["BODY_PERCENT"] = (
            CandleFeatures.body_percent(df)
        )

        df["IS_BULLISH"] = (
            CandleFeatures.bullish(df)
        )

        df["IS_BEARISH"] = (
            CandleFeatures.bearish(df)
        )
        df = MarketStructure.build(df)
        return df