from __future__ import annotations


class Statistics:

    def __init__(self):

        self.reset()


    def reset(self):

        self.total_trades = 0

        self.wins = 0
        self.losses = 0

        self.gross_profit = 0.0
        self.gross_loss = 0.0

        self.net_profit = 0.0

        self.equity_curve = []

        self.max_drawdown = 0.0



    def update(
        self,
        trades
    ):

        if trades is None:

            return


        if not isinstance(
            trades,
            list
        ):

            trades = [trades]



        for trade in trades:


            profit = float(
                getattr(
                    trade,
                    "profit",
                    0
                )
            )


            self.total_trades += 1


            self.net_profit += profit



            if profit > 0:


                self.wins += 1

                self.gross_profit += profit



            else:


                self.losses += 1

                self.gross_loss += abs(
                    profit
                )



            self.equity_curve.append(
                self.net_profit
            )



        self.calculate_drawdown()




    def calculate_drawdown(self):

        peak = 0.0

        max_dd = 0.0



        for equity in self.equity_curve:


            if equity > peak:

                peak = equity



            drawdown = peak - equity



            if drawdown > max_dd:

                max_dd = drawdown



        self.max_drawdown = max_dd





    def report(self):


        win_rate = 0.0


        if self.total_trades > 0:


            win_rate = (

                self.wins /
                self.total_trades *
                100

            )



        average_win = 0.0


        if self.wins > 0:


            average_win = (

                self.gross_profit /
                self.wins

            )



        average_loss = 0.0


        if self.losses > 0:


            average_loss = (

                self.gross_loss /
                self.losses

            )




        # -------------------------
        # Profit Factor Safe
        # -------------------------

        if self.gross_loss > 0:


            profit_factor = (

                self.gross_profit /
                self.gross_loss

            )


        elif self.gross_profit > 0:


            profit_factor = float(
                "inf"
            )


        else:


            profit_factor = 0.0





        return {


            "total_trades":
                self.total_trades,


            "wins":
                self.wins,


            "losses":
                self.losses,


            "win_rate":
                round(
                    win_rate,
                    2
                ),


            "net_profit":
                round(
                    self.net_profit,
                    2
                ),


            "gross_profit":
                round(
                    self.gross_profit,
                    2
                ),


            "gross_loss":
                round(
                    self.gross_loss,
                    2
                ),


            "average_win":
                round(
                    average_win,
                    2
                ),


            "average_loss":
                round(
                    average_loss,
                    2
                ),


            "profit_factor":

                (
                    "inf"
                    if profit_factor == float("inf")
                    else round(
                        profit_factor,
                        2
                    )
                ),



            "max_drawdown":
                round(
                    self.max_drawdown,
                    2
                )

        }




    @staticmethod
    def merge(
        reports
    ):


        result = Statistics()



        for report in reports:


            result.total_trades += report.get(
                "total_trades",
                0
            )


            result.wins += report.get(
                "wins",
                0
            )


            result.losses += report.get(
                "losses",
                0
            )


            result.gross_profit += report.get(
                "gross_profit",
                0
            )


            result.gross_loss += report.get(
                "gross_loss",
                0
            )


            result.net_profit += report.get(
                "net_profit",
                0
            )



        # بدترین DD بین فولدها
        result.max_drawdown = max(

            (
                report.get(
                    "max_drawdown",
                    0
                )

                for report in reports

            ),

            default=0

        )



        return result.report()