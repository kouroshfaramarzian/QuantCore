from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Position:
    """
    Represents an active trading position.

    مسئولیت:
    - نگهداری اطلاعات معامله
    - تغییر وضعیت باز/بسته

    بدون:
    - محاسبه سود
    - محاسبه ریسک
    - منطق خروج
    """


    symbol: str

    direction: str
    # BUY / SELL


    volume: float


    entry_price: float


    stop_loss: float


    take_profit: float


    open_time: datetime


    # -------------------------
    # Runtime State
    # -------------------------

    is_open: bool = True


    close_time: Optional[datetime] = None


    close_price: Optional[float] = None


    # -------------------------
    # Management Data
    # -------------------------

    initial_risk: float = 0.0


    highest_price: Optional[float] = None


    lowest_price: Optional[float] = None


    metadata: dict = field(
        default_factory=dict
    )


    # -------------------------
    # Update Market Price
    # -------------------------

    def update_price(
        self,
        price: float,
    ):
        """
        ذخیره High/Low حرکت معامله
        برای:
        - Trailing Stop
        - MAE/MFE
        """

        if self.highest_price is None:

            self.highest_price = price
            self.lowest_price = price

            return


        if price > self.highest_price:

            self.highest_price = price


        if price < self.lowest_price:

            self.lowest_price = price



    # -------------------------
    # Close Position
    # -------------------------

    def close(
        self,
        price: float,
        time: datetime,
    ):

        self.close_price = price

        self.close_time = time

        self.is_open = False