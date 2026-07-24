from __future__ import annotations

import pandas as pd


class SignalEngine:

    """
    QuantCore Signal Engine V7

    Logic:

    RANGE:
        HOLD


    BULL:

        Bull Structure
        +
        Fresh Bull BOS
        +
        Momentum Confirmation

        =
        BUY



    BEAR:

        Bear Structure
        +
        Fresh Bear BOS
        +
        Momentum Confirmation

        =
        SELL



    Momentum:

        MACD
        RSI
        CHOCH


    EMA:

        فقط در StructureEngine استفاده می‌شود.
        اینجا دخالت ندارد.


    BOS Freshness:

        BOS باید در آخرین N کندل باشد.
    """



    BASE_CONFIDENCE = 20

    BOS_LOOKBACK = 20



    @staticmethod
    def has_fresh_bos(
        df: pd.DataFrame,
        structure: str
    ) -> bool:


        if df is None or df.empty:

            return False



        start = max(
            0,
            len(df) - SignalEngine.BOS_LOOKBACK
        )


        recent = df.iloc[start:]



        if structure == "BULL":


            return bool(
                recent[
                    "BULLISH_BOS"
                ].any()
            )



        if structure == "BEAR":


            return bool(
                recent[
                    "BEARISH_BOS"
                ].any()
            )



        return False




    @staticmethod
    def generate(
        df: pd.DataFrame
    ) -> dict:



        if df is None or df.empty:


            return {

                "signal":"HOLD",

                "trigger":"HOLD",

                "confidence":0,

                "trend":"RANGE",

                "reason":"No data"

            }




        last = df.iloc[-1]



        structure = str(
            last.get(
                "STRUCTURE",
                "RANGE"
            )
        ).upper()



        bullish_bos = bool(
            last.get(
                "BULLISH_BOS",
                False
            )
        )


        bearish_bos = bool(
            last.get(
                "BEARISH_BOS",
                False
            )
        )



        choch_bull = bool(
            last.get(
                "CHOCH_BULLISH",
                False
            )
        )


        choch_bear = bool(
            last.get(
                "CHOCH_BEARISH",
                False
            )
        )



        macd = float(
            last.get(
                "MACD",
                0
            )
        )


        rsi = float(
            last.get(
                "RSI14",
                50
            )
        )



        confidence = int(
            last.get(
                "STRUCTURE_SCORE",
                SignalEngine.BASE_CONFIDENCE
            )
        )



        reason=[]


        signal="HOLD"




        # ==========================
        # RANGE
        # ==========================


        if structure=="RANGE":


            return {

                "signal":"HOLD",

                "trigger":"HOLD",

                "confidence":confidence,

                "trend":structure,

                "reason":"Range Market"

            }





        # ==========================
        # BULL
        # ==========================


        if structure=="BULL":



            reason.append(
                "Bull Structure"
            )



            fresh_bos = SignalEngine.has_fresh_bos(
                df,
                "BULL"
            )



            if not fresh_bos:


                reason.append(
                    "Waiting Fresh Bull BOS"
                )


                return {

                    "signal":"HOLD",

                    "trigger":"HOLD",

                    "confidence":confidence,

                    "trend":structure,

                    "reason":", ".join(reason)

                }



            reason.append(
                "Bull BOS Confirmed"
            )



            confirmation=False




            if macd > 0:


                confirmation=True


                reason.append(
                    "MACD Bull"
                )



            if rsi > 55:


                confirmation=True


                reason.append(
                    "RSI Bull"
                )



            if choch_bull:


                confirmation=True


                reason.append(
                    "Bull CHOCH"
                )




            if confirmation:


                signal="BUY"


                confidence=min(
                    confidence+20,
                    100
                )



            else:


                reason.append(
                    "Waiting Momentum"
                )






        # ==========================
        # BEAR
        # ==========================


        elif structure=="BEAR":



            reason.append(
                "Bear Structure"
            )



            fresh_bos = SignalEngine.has_fresh_bos(
                df,
                "BEAR"
            )



            if not fresh_bos:


                reason.append(
                    "Waiting Fresh Bear BOS"
                )


                return {


                    "signal":"HOLD",

                    "trigger":"HOLD",

                    "confidence":confidence,

                    "trend":structure,

                    "reason":", ".join(reason)

                }



            reason.append(
                "Bear BOS Confirmed"
            )



            confirmation=False




            if macd < 0:


                confirmation=True


                reason.append(
                    "MACD Bear"
                )



            if rsi < 45:


                confirmation=True


                reason.append(
                    "RSI Bear"
                )



            if choch_bear:


                confirmation=True


                reason.append(
                    "Bear CHOCH"
                )





            if confirmation:


                signal="SELL"


                confidence=min(
                    confidence+20,
                    100
                )



            else:


                reason.append(
                    "Waiting Momentum"
                )





        else:


            reason.append(
                "Unknown Structure"
            )





        return {


            "signal":signal,


            "trigger":signal,


            "confidence":confidence,


            "trend":structure,


            "reason":", ".join(reason)


        }






    @staticmethod
    def generate_series(
        df: pd.DataFrame
    ) -> pd.DataFrame:



        df=df.copy()


        signals=[]

        triggers=[]

        confidences=[]

        trends=[]

        reasons=[]



        for i in range(len(df)):



            result = SignalEngine.generate(

                df.iloc[:i+1]

            )



            signals.append(
                result["signal"]
            )


            triggers.append(
                result["trigger"]
            )


            confidences.append(
                result["confidence"]
            )


            trends.append(
                result["trend"]
            )


            reasons.append(
                result["reason"]
            )




        df["signal"]=signals

        df["trigger"]=triggers

        df["confidence"]=confidences

        df["trend"]=trends

        df["reason"]=reasons



        return df