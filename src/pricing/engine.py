from src.pricing.pnl import PnLCalculator
from src.pricing.spread import SpreadCalculator
from src.pricing.commission import CommissionCalculator
from src.pricing.slippage import SlippageCalculator


class PricingEngine:

    def __init__(self):

        self.pnl = PnLCalculator()

        self.spread = SpreadCalculator()

        self.commission = CommissionCalculator()

        self.slippage = SlippageCalculator()

    def calculate_trade_result(

        self,

        position,

        bid,

        ask,

    ):

        exit_price = self.spread.apply(

            position.direction,

            bid,

            ask,

        )

        exit_price = self.slippage.apply(exit_price)

        gross_profit = self.pnl.calculate(

            position,

            exit_price,

        )

        commission = self.commission.calculate(

            position.volume,

        )

        net_profit = gross_profit - commission

        return {

            "exit_price": exit_price,

            "gross_profit": gross_profit,

            "commission": commission,

            "net_profit": net_profit,

        }