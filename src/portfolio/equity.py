from __future__ import annotations


class EquityEngine:

    """
    Calculates floating equity.
    """

    def __init__(self):

        self.balance = 0.0

        self.equity = 0.0

        self.floating_profit = 0.0

        self.closed_profit = 0.0

    def update(

        self,

        account,

        positions,

        pricing_engine,

        bid,

        ask,

    ):

        floating = 0.0

        for position in positions:

            if not position.is_open:

                continue

            pnl = pricing_engine.pnl.calculate(

                position,

                bid if position.direction == "SELL" else ask,

            )

            position.floating_profit = pnl

            floating += pnl

        self.balance = account.balance

        self.closed_profit = account.balance

        self.floating_profit = floating

        self.equity = account.balance + floating