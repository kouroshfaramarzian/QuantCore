import pandas as pd


class DataValidator:
    """
    Validate market data before entering the pipeline.
    """

    REQUIRED_COLUMNS = [
        "time",
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]

    @classmethod
    def validate(cls, df: pd.DataFrame) -> bool:

        # Empty dataframe
        if df.empty:
            raise ValueError("DataFrame is empty.")

        # Required columns
        missing = [
            col for col in cls.REQUIRED_COLUMNS
            if col not in df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing columns: {missing}"
            )

        # Null values
        if df.isnull().values.any():
            raise ValueError(
                "DataFrame contains NaN values."
            )

        # Duplicate timestamps
        if df["time"].duplicated().any():
            raise ValueError(
                "Duplicate timestamps detected."
            )

        return True