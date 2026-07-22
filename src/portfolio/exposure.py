from collections import defaultdict


class ExposureEngine:

    """
    Calculates portfolio exposure.
    """

    def __init__(self):

        self.reset()

    def reset(self):

        self.symbol_volume = defaultdict(float)

        self.buy_volume = 0.0

        self.sell_volume = 0.0

    def rebuild(self, positions):

        self.reset()

        for position in positions:

            if not position.is_open:
                continue

            self.symbol_volume[position.symbol] += position.volume

            if position.direction == "BUY":

                self.buy_volume += position.volume

            else:

                self.sell_volume += position.volume

    def total_volume(self):

        return self.buy_volume + self.sell_volume

    def symbol_exposure(

        self,

        symbol,

    ):

        return self.symbol_volume[symbol]