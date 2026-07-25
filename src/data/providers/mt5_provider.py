import MetaTrader5 as mt5
import pandas as pd

from src.data.providers.base_provider import BaseProvider


class MT5Provider(BaseProvider):
    """
    MetaTrader5 market data provider.
    """


    def connect(self) -> bool:

        if not mt5.initialize():

            raise ConnectionError(
                "Cannot initialize MetaTrader5."
            )

        return True



    def disconnect(self) -> None:

        mt5.shutdown()



    # سازگاری با main.py
    def shutdown(self):

        self.disconnect()



    def load_data(
        self,
        symbol: str,
        timeframe,
        start=None,
        end=None,
        count: int = 1000,
    ) -> pd.DataFrame:


        rates = mt5.copy_rates_from_pos(
            symbol,
            timeframe,
            0 if start is None else start,
            count,
        )


        if rates is None:

            raise RuntimeError(
                f"Cannot load data for {symbol}"
            )



        df = pd.DataFrame(
            rates
        )



        df = df.rename(
            columns={
                "tick_volume": "volume",
            }
        )



        df["time"] = pd.to_datetime(
            df["time"],
            unit="s"
        )



        df = df[
            [
                "time",
                "open",
                "high",
                "low",
                "close",
                "volume",
            ]
        ]



        return df