from pathlib import Path

import pandas as pd


class DataManager:
    """
    Save and load historical market data.
    """

    def __init__(self, data_dir="datasets/raw"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def build_filename(
        self,
        symbol: str,
        timeframe: str,
    ) -> Path:

        return self.data_dir / f"{symbol}_{timeframe}.csv"

    def save(
        self,
        df: pd.DataFrame,
        symbol: str,
        timeframe: str,
    ):

        file = self.build_filename(
            symbol,
            timeframe,
        )

        df.to_csv(file, index=False)

        return file

    def load(
        self,
        symbol: str,
        timeframe: str,
    ) -> pd.DataFrame:

        file = self.build_filename(
            symbol,
            timeframe,
        )

        return pd.read_csv(file)