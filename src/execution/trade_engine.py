from src.execution.lifecycle import TradeLifecycle
from src.pricing.engine import PricingEngine


class TradeEngine:

    """
    Responsible for closing trades.
    """

    def __init__(self):

        self.pricing = PricingEngine()

        self.lifecycle = TradeLifecycle()

    def close(

        self,

        position,

        bid,

        ask,

        time,

    ):

        result = self.pricing.calculate_trade_result(

            position,

            bid,

            ask,

        )

        trade = self.lifecycle.close(

            position,

            result["exit_price"],

            time,

        )

        trade.gross_profit = result["gross_profit"]

        trade.net_profit = result["net_profit"]

        trade.commission = result["commission"]

        return trade