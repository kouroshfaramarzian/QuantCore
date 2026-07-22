from src.domain.position import Position


class PnLCalculator:

    def calculate(

        self,

        position: Position,

        exit_price: float,

    ) -> float:

        if position.direction == "BUY":

            return exit_price - position.entry_price

        return position.entry_price - exit_price