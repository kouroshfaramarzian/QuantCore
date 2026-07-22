class ExecutionEngine:

    def __init__(

        self,

        validator,

        order_factory,

        order_manager,

        position_manager,

    ):

        self.validator = validator

        self.factory = order_factory

        self.orders = order_manager

        self.positions = position_manager

    def execute(

        self,

        strategy_decision,

        account,

        contract,

        market,

        symbol,

        volume,

    ):

        validation = self.validator.validate(

            account,

            contract,

            strategy_decision.risk,

            market,

        )

        if not validation.accepted:

            return None

        order = self.factory.create(

            strategy_decision.signal,

            strategy_decision.risk,

            symbol,

            volume,

        )

        position = self.orders.execute(order)

        self.positions.open(position)

        return position