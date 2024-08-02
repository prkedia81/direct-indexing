import datetime as dt
import pandas as pd
import numpy as np

# Initialise Cash
cash_col = ["Date", "Description", "Debit", "Credit", "Balance"]
cash_df = pd.DataFrame(columns=cash_col)
cash_df = cash_df.append(
    pd.Series(
        [
            dt.datetime.today().strftime("%d/%m/%Y"),
            "Opening Balance",
            np.nan,
            np.nan,
            2500000.0
        ], index=cash_col,
    ),
    ignore_index=True
)
cash_df.to_csv("Cash.csv", index=False)

# Initialise Master

# Initialise
