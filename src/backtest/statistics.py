from typing import List

from src.backtest.trade import Trade


class Statistics:
    """
    Calculates backtest statistics.
    """

    @staticmethod
    def calculate(
        trades: List[Trade],
    ) -> dict:

        if len(trades) == 0:

            return {

                "total_trades": 0,

                "wins": 0,

                "losses": 0,

                "win_rate": 0,

                "net_profit": 0,

                "average_win": 0,

                "average_loss": 0,

                "profit_factor": 0,

            }

        wins = [
            t for t in trades
            if t.result == "WIN"
        ]

        losses = [
            t for t in trades
            if t.result == "LOSS"
        ]

        total_profit = sum(
            t.profit for t in wins
        )

        total_loss = abs(
            sum(
                t.profit
                for t in losses
            )
        )

        win_rate = (
            len(wins)
            / len(trades)
            * 100
        )

        average_win = (

            total_profit / len(wins)

            if wins else 0

        )

        average_loss = (

            total_loss / len(losses)

            if losses else 0

        )

        profit_factor = (

            total_profit / total_loss

            if total_loss > 0 else 0

        )

        return {

            "total_trades": len(trades),

            "wins": len(wins),

            "losses": len(losses),

            "win_rate": round(win_rate, 2),

            "net_profit": round(
                total_profit - total_loss,
                2,
            ),

            "average_win": round(
                average_win,
                2,
            ),

            "average_loss": round(
                average_loss,
                2,
            ),

            "profit_factor": round(
                profit_factor,
                2,
            ),

        }