from __future__ import annotations

import pandas as pd

from .swing import SwingDetector
from .bos import BOSDetector
from .choch import CHOCHDetector


class MarketStructure:

    @staticmethod
    def build(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df = SwingDetector.detect(df)

        df = BOSDetector.detect(df)

        df = CHOCHDetector.detect(df)

        return df