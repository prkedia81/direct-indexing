import datetime as dt
import pandas as pd
import numpy as np


class Cash:
    def __init__(self):
        with open("Cash.csv", "r") as cash_file:
            self.cash_df = pd.read_csv(cash_file)
        self.cash_col = ["Date", "Description", "Debit", "Credit", "Balance"]

    def debit(self, description: str, debit: float):
        """Cash going out -> Buying Shares. Parameters: Description, Amount Debited"""

        self.cash_df.append(
            pd.Series(
                [
                    dt.datetime.today().strftime("%d/%m/%Y"),
                    description,
                    debit,
                    np.nan,
                    # float(self.cash_df.loc[len(self.cash_df.index) - 1, "Balance"] - debit)
                    2500000
                ], index=self.cash_col
            ),
            ignore_index=True
        )

    def credit(self, description: str, credit: float):
        """Cash coming in -> Selling Shares. Parameters: Description, Amount Debited"""

        self.cash_df.append(
            pd.Series(
                [
                    dt.datetime.today().strftime("%d/%m/%Y"),
                    description,
                    credit,
                    np.nan,
                    float(self.cash_df.loc[len(self.cash_df.index) - 1, "Balance"] + credit)
                ], index=self.cash_col
            ),
            ignore_index=True
        )

    def cash_available(self) -> float:
        """Returns the balance of the last entry."""
        cash = float(self.cash_df.loc[len(self.cash_df.index) - 1, "Balance"])
        return cash

    def save_cash_ledger(self):
        """Updates 'Cash.csv' at the end of the rebalancing"""
        self.cash_df.to_csv("Cash.csv", index=False)
