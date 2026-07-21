from dataclasses import dataclass

import pandas as pd


@dataclass
class ExecutionResult:
    """
    Result of one simulated trade.
    """

    exit_price: float

    exit_index: int

    result: str

    profit: float


class TradeExecutor:
    """
    Executes one historical trade.
    """

    @staticmethod
    def execute_buy(
        df: pd.DataFrame,
        entry_index: int,
        entry: float,
        stop_loss: float,
        take_profit: float,
    ) -> ExecutionResult:

        for i in range(entry_index + 1, len(df)):

            candle = df.iloc[i]

            # Stop Loss

            if candle["low"] <= stop_loss:

                return ExecutionResult(

                    exit_price=stop_loss,

                    exit_index=i,

                    result="LOSS",

                    profit=stop_loss - entry,

                )

            # Take Profit

            if candle["high"] >= take_profit:

                return ExecutionResult(

                    exit_price=take_profit,

                    exit_index=i,

                    result="WIN",

                    profit=take_profit - entry,

                )

        # No exit until end

        last = df.iloc[-1]

        return ExecutionResult(

            exit_price=last["close"],

            exit_index=len(df) - 1,

            result="OPEN",

            profit=last["close"] - entry,

        )

    @staticmethod
    def execute_sell(
        df: pd.DataFrame,
        entry_index: int,
        entry: float,
        stop_loss: float,
        take_profit: float,
    ) -> ExecutionResult:

        for i in range(entry_index + 1, len(df)):

            candle = df.iloc[i]

            if candle["high"] >= stop_loss:

                return ExecutionResult(

                    exit_price=stop_loss,

                    exit_index=i,

                    result="LOSS",

                    profit=entry - stop_loss,

                )

            if candle["low"] <= take_profit:

                return ExecutionResult(

                    exit_price=take_profit,

                    exit_index=i,

                    result="WIN",

                    profit=entry - take_profit,

                )

        last = df.iloc[-1]

        return ExecutionResult(

            exit_price=last["close"],

            exit_index=len(df) - 1,

            result="OPEN",

            profit=entry - last["close"],

        )