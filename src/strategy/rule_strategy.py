from src.strategy.base_strategy import BaseStrategy
from src.strategy.signal_engine import SignalEngine
from src.risk.risk_engine import RiskEngine


class RuleStrategy(BaseStrategy):
    """
    Default QuantCore Rule Based Strategy.
    """

    def generate(self, df):

        signal = SignalEngine.generate(df)

        risk = RiskEngine.calculate(

            df,

            signal["signal"].value,

        )

        return {

            "signal": signal,

            "risk": risk,

        }