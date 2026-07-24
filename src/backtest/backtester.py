from src.backtest.engine import TradingEngine
from src.backtest.position import Position

from src.risk.risk_engine import RiskEngine



class Backtester:


    def __init__(self):

        self.engine = TradingEngine()



    def run(
        self,
        df
    ):

        self.engine.reset()


        for i in range(1, len(df)):


            candle = df.iloc[i]


            time = candle.name


            signal = candle.get(
                "signal",
                "HOLD"
            )


            high = candle["high"]

            low = candle["low"]

            close = candle["close"]



            # =====================================
            # MANAGE OPEN POSITION
            # =====================================

            if self.engine.position is not None:


                pos = self.engine.position



                # BUY

                if pos.direction == "BUY":


                    if low <= pos.stop_loss:


                        self.engine.close_position(
                            pos.stop_loss,
                            time
                        )


                    elif high >= pos.take_profit:


                        self.engine.close_position(
                            pos.take_profit,
                            time
                        )



                # SELL

                elif pos.direction == "SELL":


                    if high >= pos.stop_loss:


                        self.engine.close_position(
                            pos.stop_loss,
                            time
                        )


                    elif low <= pos.take_profit:


                        self.engine.close_position(
                            pos.take_profit,
                            time
                        )



            # =====================================
            # OPEN POSITION
            # =====================================

            if self.engine.position is None:


                if signal in (
                    "BUY",
                    "SELL"
                ):



                    print(
                        "TRADE:",
                        time,
                        signal,
                        "STRUCTURE:",
                        candle.get(
                            "STRUCTURE"
                        ),
                        "BOS:",
                        candle.get(
                            "BULLISH_BOS"
                        ),
                        candle.get(
                            "BEARISH_BOS"
                        )
                    )



                    risk = RiskEngine.calculate(

                        df.iloc[:i+1],

                        signal

                    )



                    if (
                        risk["entry"]
                        is None
                    ):

                        continue



                    position = Position(

                        symbol="XAUUSD",

                        direction=signal,

                        volume=1.0,

                        entry_price=risk["entry"],

                        stop_loss=risk["stop_loss"],

                        take_profit=risk["take_profit"],

                        open_time=time

                    )


                    self.engine.open_position(
                        position
                    )




        # =====================================
        # CLOSE REMAINING POSITION
        # =====================================

        if self.engine.position is not None:


            last = df.iloc[-1]


            self.engine.close_position(

                last["close"],

                last.name

            )



        return self.engine.trades



    def statistics(self):

        return self.engine.report()