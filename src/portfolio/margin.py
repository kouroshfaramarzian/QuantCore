class MarginEngine:

    """
    Margin calculations.
    """

    def __init__(self):

        self.used_margin = 0.0

        self.free_margin = 0.0

        self.margin_level = 0.0

    def update(

        self,

        account,

        positions,

        contract,

    ):

        used = 0.0

        for position in positions:

            if not position.is_open:

                continue

            used += (

                contract.contract_size

                * position.volume

                * position.entry_price

            ) / account.leverage

        self.used_margin = used

        self.free_margin = account.equity - used

        if used > 0:

            self.margin_level = (

                account.equity

                / used

            ) * 100

        else:

            self.margin_level = 0