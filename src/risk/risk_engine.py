import pandas as pd


class RiskEngine:
    """
    Calculates entry, stop loss and take profit.
    """

    @staticmethod
    def calculate(
        df: pd.DataFrame,
        signal: str,
        rr: float = 2.0,
        atr_multiplier: float = 2.0,
    ) -> dict:

        last = df.iloc[-1]

        entry = last["close"]

        atr = last["ATR14"]

        if signal == "BUY":

            stop_loss = entry - atr * atr_multiplier

            take_profit = (
                entry
                + (entry - stop_loss) * rr
            )

        elif signal == "SELL":

            stop_loss = entry + atr * atr_multiplier

            take_profit = (
                entry
                - (stop_loss - entry) * rr
            )

        else:

            return {
                "entry": None,
                "stop_loss": None,
                "take_profit": None,
            }

        return {

            "entry": round(entry, 2),

            "stop_loss": round(stop_loss, 2),

            "take_profit": round(take_profit, 2),

        }