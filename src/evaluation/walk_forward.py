from src.backtest.backtester import Backtester
from src.backtest.statistics import Statistics


class WalkForwardValidator:
    """
    Walk Forward Validation
    """

    @staticmethod
    def run(
        df,
        train_size=700,
        test_size=300,
        step=300,
    ):

        results = []

        start = 0

        while start + train_size + test_size <= len(df):

            train = df.iloc[start:start + train_size]

            test = df.iloc[
                start + train_size:
                start + train_size + test_size
            ]

            backtester = Backtester()

            trades = backtester.run(test)

            stats = Statistics.calculate(trades)

            results.append(stats)

            start += step

        return results