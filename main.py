import pandas as pd
import numpy as np
from scraping import Scraper
from operations import Operations

# scrape = Scraper()
# sensex_list = scrape.bse_sensex_list()
# print("Got Sensex List")
#
# column_list = ['Name', 'Ticker Symbol', 'Price (in Rs)', 'FF Market Cap (in Cr)', '% by Market Cap']
# today_df = pd.DataFrame(columns=column_list)
#
# for stock in sensex_list:
#     if stock == "INFY*":
#         stock = "INFY"
#     stock_dict = scrape.stock_scraper(stock)
#
#     today_df = today_df.append(
#         pd.Series(
#             [
#                 stock_dict["name"],
#                 stock_dict["ticker_symbol"],
#                 stock_dict["price"],
#                 stock_dict["ff_market_cap"],
#                 np.nan,
#             ],
#             index=column_list
#         ),
#         ignore_index=True,
#     )
#     print(stock_dict["name"])
#
# # Calculating and Assigning Weightage as of Today
# total_market_cap = today_df["FF Market Cap (in Cr)"].sum()
# for i in range(30):
#     market_weight_percent = round(((today_df["FF Market Cap (in Cr)"][i] / total_market_cap) * 100), 2)
#     today_df.loc[i, "% by Market Cap"] = market_weight_percent
# today_df.sort_values(by="% by Market Cap", ascending=False, inplace=True, ignore_index=True)

with open('Today.csv', 'r') as today:
    today_df = pd.read_csv(today)

operate = Operations(today_df)
operate.quantity_assign()
is_capital_available = operate.cash_check()
if is_capital_available is True:
    operate.rebalance()
operate.master_updation()
