from __future__ import annotations


class Statistics:

    def __init__(self):

        self.reset()

    def reset(self):

        self.total_trades = 0

        self.wins = 0

        self.losses = 0

        self.net_profit = 0.0

        self.gross_profit = 0.0

        self.gross_loss = 0.0

        self.average_win = 0.0

        self.average_loss = 0.0

        self.profit_factor = 0.0

        self.win_rate = 0.0

    def update(self, trade):

        self.total_trades += 1

        self.net_profit += trade.profit

        if trade.profit > 0:

            self.wins += 1

            self.gross_profit += trade.profit

        else:

            self.losses += 1

            self.gross_loss += abs(trade.profit)

        self._calculate()

    def _calculate(self):

        if self.total_trades:

            self.win_rate = self.wins / self.total_trades * 100

        if self.wins:

            self.average_win = self.gross_profit / self.wins

        if self.losses:

            self.average_loss = self.gross_loss / self.losses

        if self.gross_loss > 0:

            self.profit_factor = self.gross_profit / self.gross_loss

        elif self.gross_profit > 0:

            self.profit_factor = float("inf")

        else:

            self.profit_factor = 0

    def summary(

        self,

        portfolio=None,

    ):

        report = {

            "total_trades": self.total_trades,

            "wins": self.wins,

            "losses": self.losses,

            "win_rate": round(self.win_rate, 2),

            "net_profit": round(self.net_profit, 2),

            "gross_profit": round(self.gross_profit, 2),

            "gross_loss": round(self.gross_loss, 2),

            "average_win": round(self.average_win, 2),

            "average_loss": round(self.average_loss, 2),

            "profit_factor": (
                round(self.profit_factor, 2)
                if self.profit_factor != float("inf")
                else "INF"
            ),

        }

        if portfolio is not None:

            report.update(

                portfolio.summary()

            )

        return report