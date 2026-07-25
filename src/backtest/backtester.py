from __future__ import annotations

from src.backtest.engine import TradingEngine
from src.backtest.position import Position

from src.risk.risk_engine import RiskEngine
from src.strategy.decision_engine import DecisionEngine



class Backtester:


    def __init__(self):

        self.engine = TradingEngine()



    def run(
        self,
        df
    ):


        self.engine.reset()


        for i in range(
            1,
            len(df) - 1
        ):


            signal_candle = df.iloc[i]


            execution_candle = df.iloc[i + 1]


            signal_time = signal_candle.name


            execution_time = execution_candle.name



            signal = signal_candle.get(
                "signal",
                "HOLD"
            )


            confidence = int(
                signal_candle.get(
                    "confidence",
                    0
                )
            )


            trend = signal_candle.get(
                "trend",
                "RANGE"
            )


            reason = signal_candle.get(
                "reason",
                ""
            )



            decision = DecisionEngine.decide(

                signal=signal,

                confidence=confidence,

                trend=trend,

                reason=reason

            )



            final_signal = decision.get(
                "signal",
                "HOLD"
            )



            high = signal_candle["high"]

            low = signal_candle["low"]




            # ============================
            # CLOSE POSITION
            # ============================


            if self.engine.position is not None:


                position = self.engine.position



                if position.direction == "BUY":


                    if low <= position.stop_loss:


                        self.engine.close_position(

                            position.stop_loss,

                            signal_time

                        )


                    elif high >= position.take_profit:


                        self.engine.close_position(

                            position.take_profit,

                            signal_time

                        )





                elif position.direction == "SELL":


                    if high >= position.stop_loss:


                        self.engine.close_position(

                            position.stop_loss,

                            signal_time

                        )


                    elif low <= position.take_profit:


                        self.engine.close_position(

                            position.take_profit,

                            signal_time

                        )







            # ============================
            # OPEN POSITION
            # ============================


            if self.engine.position is None:



                if final_signal not in (

                    "BUY",

                    "SELL"

                ):

                    continue




                # ورود واقعی:
                # open کندل بعد از سیگنال


                entry_price = float(

                    execution_candle["open"]

                )




                risk = RiskEngine.calculate(

                    df.iloc[:i + 1],

                    final_signal,

                    entry_price=entry_price

                )



                if risk["entry"] is None:

                    continue




                print(

                    "TRADE:",

                    signal_time,

                    final_signal,

                    "ENTRY:",

                    risk["entry"],

                    "STRUCTURE:",

                    signal_candle.get(
                        "STRUCTURE"
                    ),

                    "DECISION:",

                    decision

                )





                position = Position(

                    symbol="XAUUSD",

                    direction=final_signal,

                    volume=1.0,

                    entry_price=risk["entry"],

                    stop_loss=risk["stop_loss"],

                    take_profit=risk["take_profit"],

                    open_time=execution_time

                )



                self.engine.open_position(

                    position

                )






        # ============================
        # CLOSE LAST POSITION
        # ============================


        if self.engine.position is not None:


            last = df.iloc[-1]


            self.engine.close_position(

                last["close"],

                last.name

            )



        return self.engine.trades




    def statistics(self):

        return self.engine.report()