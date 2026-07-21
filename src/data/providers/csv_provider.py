from pathlib import Path

import pandas as pd

from src.data.providers.base_provider import BaseProvider


class CSVProvider(BaseProvider):
    """
    CSV market data provider.
    """

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def connect(self) -> bool:
        if not self.file_path.exists():
            raise FileNotFoundError(f"{self.file_path} not found")

        return True

    def disconnect(self) -> None:
        pass

    def load_data(
        self,
        symbol: str = "",
        timeframe: str = "",
        start=None,
        end=None,
    ) -> pd.DataFrame:

        if not self.file_path.exists():
            raise FileNotFoundError(f"{self.file_path} not found")

        df = pd.read_csv(self.file_path)

        return df