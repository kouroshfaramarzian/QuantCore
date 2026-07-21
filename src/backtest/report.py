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

        print(f"Total Trades   : {stats['total_trades']}")

        print(f"Wins           : {stats['wins']}")

        print(f"Losses         : {stats['losses']}")

        print(f"Win Rate       : {stats['win_rate']} %")

        print("-" * 60)

        print(f"Net Profit     : {stats['net_profit']}")

        print(f"Average Win    : {stats['average_win']}")

        print(f"Average Loss   : {stats['average_loss']}")

        print(f"Profit Factor  : {stats['profit_factor']}")

        print("=" * 60)