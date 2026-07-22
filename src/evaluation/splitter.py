import pandas as pd


class DataSplitter:
    """
    Splits dataset into
    train / validation / test.
    """

    @staticmethod
    def split(

        df: pd.DataFrame,

        train_size: float = 0.7,

        validation_size: float = 0.15,

    ):

        total = len(df)

        train_end = int(total * train_size)

        validation_end = int(

            total *

            (train_size + validation_size)

        )

        train = df.iloc[:train_end].copy()

        validation = df.iloc[

            train_end:validation_end

        ].copy()

        test = df.iloc[validation_end:].copy()

        return (

            train,

            validation,

            test,

        )