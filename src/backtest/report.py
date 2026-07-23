class Report:
    """
    Pretty prints backtest statistics.
    """

    @staticmethod
    def show(stats: dict) -> None:

        print()

        print("=" * 60)
        print("            QuantCore Backtest Report")
        print("=" * 60)

        print(f"Initial Balance : {stats.get('initial_balance', '-')}")
        print(f"Final Balance   : {stats.get('balance', '-')}")
        print(f"Equity          : {stats.get('equity', '-')}")

        print("-" * 60)

        print(f"Total Trades    : {stats.get('total_trades', 0)}")
        print(f"Wins            : {stats.get('wins', 0)}")
        print(f"Losses          : {stats.get('losses', 0)}")
        print(f"Win Rate        : {stats.get('win_rate', 0)} %")

        print("-" * 60)

        print(f"Net Profit      : {stats.get('net_profit', 0)}")
        print(f"Gross Profit    : {stats.get('gross_profit', 0)}")
        print(f"Gross Loss      : {stats.get('gross_loss', 0)}")

        print("-" * 60)

        print(f"Average Win     : {stats.get('average_win', 0)}")
        print(f"Average Loss    : {stats.get('average_loss', 0)}")
        print(f"Profit Factor   : {stats.get('profit_factor', 0)}")
        print(f"Max Drawdown    : {stats.get('max_drawdown', 0)}")

        print("=" * 60)