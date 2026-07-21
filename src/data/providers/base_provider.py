from abc import ABC, abstractmethod
import pandas as pd


class BaseProvider(ABC):
    """
    Abstract base class for all market data providers.
    """

    @abstractmethod
    def connect(self) -> bool:
        """Connect to data source."""
        raise NotImplementedError

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from data source."""
        raise NotImplementedError

    @abstractmethod
    def load_data(
        self,
        symbol: str,
        timeframe: str,
        start,
        end,
    ) -> pd.DataFrame:
        """
        Load market data and return a pandas DataFrame.
        """
        raise NotImplementedError