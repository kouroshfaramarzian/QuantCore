import pandas as pd

from src.data.providers.base_provider import BaseProvider
from src.data.validator import DataValidator


class DataPipeline:
    """
    Complete data loading pipeline.
    """

    def __init__(self, provider: BaseProvider):
        self.provider = provider

    def run(
        self,
        symbol: str = "",
        timeframe: str = "",
        start=None,
        end=None,
    ) -> pd.DataFrame:

        self.provider.connect()

        df = self.provider.load_data(
            symbol=symbol,
            timeframe=timeframe,
            start=start,
            end=end,
        )

        DataValidator.validate(df)

        self.provider.disconnect()

        return df