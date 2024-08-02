import sqlite3
import pandas as pd

master_db = sqlite3.connect("master.db")
master = master_db.cursor()
master.execute("CREATE TABLE share_list ("
               "ticker_symbol NOT NULL UNIQUE,"
               "name TEXT,"
               "price REAL,"
               "ff_market_cap REAL,"
               "percent_by_market_cap REAL)"
               )

master.execute("CREATE TABLE holdings ("
               "ticker_symbol NOT NULL UNIQUE,"
               "buy_price REAL,"
               "quantity REAL)"
               )

with open('Master DataFrame Original.csv', 'r') as file:
    master_df = pd.read_csv(file)

for i in range(30):
    share_list_tuple = (
        master_df["Ticker Symbol"][i],
        master_df["Name"][i],
        master_df["Price (in Rs)"][i],
        master_df["FF Market Cap (in Cr)"][i],
        master_df["% by Market Cap"][i]
    )
    master.execute("INSERT INTO share_list VALUES (?, ?, ?, ?, ?)", share_list_tuple)
    holdings_tuple = (
        master_df["Ticker Symbol"][i],
        master_df["Buy Price"][i],
        master_df["Quantity"][i]
    )
    master.execute("INSERT INTO holdings VALUES (?,?,?)", holdings_tuple)

master_db.commit()
