class BacktestEngine:

    """
    Trade execution engine.
    """

    def __init__(self):

        self.position = None

    def has_position(self):

        return self.position is not None

    def open_position(

        self,

        position,

    ):

        self.position = position

    def close_position(self):

        position = self.position

        self.position = None

        return position