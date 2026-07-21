from typing import List

import pandas as pd

from src.backtest.trade import Trade
from src.backtest.executor import TradeExecutor

from src.features.feature_engine import FeatureEngine

from src.strategy.signal_engine import SignalEngine

from src.risk.risk_engine import RiskEngine


class Backtester:
    """
    Historical Backtesting Engine.
    """

    def __init__(self):

        self.trades: List[Trade] = []

    def run(
        self,
        df: pd.DataFrame,
    ) -> List[Trade]:

        self.trades.clear()

        # از کندل 200 شروع می‌کنیم
        # تا EMA200 مقدار داشته باشد

        for i in range(200, len(df) - 1):

            history = df.iloc[: i + 1].copy()

            history = FeatureEngine.transform(history)

            signal = SignalEngine.generate(history)

            direction = signal["signal"].value

            if direction == "HOLD":

                continue

            risk = RiskEngine.calculate(
                history,
                direction,
            )

            if risk["entry"] is None:

                continue

            if direction == "BUY":

                execution = TradeExecutor.execute_buy(

                    df,

                    i,

                    risk["entry"],

                    risk["stop_loss"],

                    risk["take_profit"],

                )

            else:

                execution = TradeExecutor.execute_sell(

                    df,

                    i,

                    risk["entry"],

                    risk["stop_loss"],

                    risk["take_profit"],

                )

            trade = Trade(

                symbol="XAUUSD",

                timeframe="M1",

                direction=direction,

                entry_time=df.iloc[i]["time"],

                exit_time=df.iloc[
                    execution.exit_index
                ]["time"],

                entry_price=risk["entry"],

                exit_price=execution.exit_price,

                stop_loss=risk["stop_loss"],

                take_profit=risk["take_profit"],

                volume=1.0,

                profit=execution.profit,

                rr=2.0,

                result=execution.result,

            )

            self.trades.append(trade)

        return self.trades