from __future__ import annotations


from src.backtest.backtester import Backtester
from src.backtest.statistics import Statistics
from src.strategy.signal_engine import SignalEngine



class WalkForwardValidator:
    """
    QuantCore Walk Forward Validator V3


    تغییرات:

    - اضافه شدن context window
    - حفظ state ساختاری
    - اجرای SignalEngine روی context + test
    - محاسبه معامله فقط روی test
    """



    @staticmethod
    def run(

        df,

        train_size=700,

        test_size=300,

        step=300,

        context_size=100

    ):


        results = []


        start = 0


        fold_id = 1




        while (

            start +
            train_size +
            test_size

            <= len(df)

        ):



            train_start = start


            train_end = (

                start +
                train_size

            )


            test_end = (

                train_end +
                test_size

            )



            # -----------------------------
            # Train
            # -----------------------------

            train = df.iloc[

                train_start:

                train_end

            ].copy()




            # -----------------------------
            # Context + Test
            # -----------------------------

            context_start = max(

                0,

                train_end -
                context_size

            )



            test_context = df.iloc[

                context_start:

                test_end

            ].copy()




            print(

                "WF FOLD:",

                fold_id,

                "TRAIN:",

                len(train),

                "CONTEXT:",

                context_start,

                "-",

                train_end - 1,

                "TEST:",

                train_end,

                "-",

                test_end - 1

            )





            # ---------------------------------
            # Rebuild Signals
            # ---------------------------------

            processed = SignalEngine.generate_series(

                test_context

            )





            # ---------------------------------
            # Remove context trades
            # ---------------------------------

            execution_data = processed.loc[

                processed.index >= df.index[train_end]

            ].copy()




            backtester = Backtester()



            trades = backtester.run(

                execution_data

            )



            stats = Statistics()



            stats.update(

                trades

            )



            report = stats.report()



            report["fold"] = fold_id


            report["train_size"] = len(train)


            report["context_size"] = context_size


            report["test_size"] = test_size


            report["trades_count"] = len(trades)



            results.append(

                report

            )



            fold_id += 1


            start += step





        aggregate = Statistics.merge(

            results

        )



        return {


            "folds":

                results,


            "aggregate":

                aggregate

        }