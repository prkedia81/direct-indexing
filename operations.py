import pandas as pd
import math
from cash import Cash


class Operations:
    def __init__(self, today_df):
        self.today_df = today_df
        self.ledger = Cash()
        with open('Master DataFrame.csv', 'r') as mdf_csv:
            self.master_df = pd.read_csv(mdf_csv)
        flag = False
        for i in range(30):
            weight_master = self.master_df["% by Market Cap"][i]
            weight_data = self.today_df["% by Market Cap"][i]
            if abs(weight_master - weight_data) >= 0.01:  # To be changed to 0.5
                flag = True
                break
        if flag is not True:
            return

        self.cash = self.ledger.cash_available()
        # index: quantity to buy or sell
        self.sell_loss = {}
        self.sell_profit = {}
        self.buy = {}

    def quantity_assign(self):
        """Assign quantity to the shares according to today's weightage."""

        # We will need Rs 25 Lakh to start tracking and buy atleast 1 unit of the index
        beginning_capital = 2500000
        # Eventually with capital gain, this will have to change

        # Assigning quantity one should hold today.
        self.today_df["Quantity"] = 0
        cash_spent = 0
        for i in range(30):
            weight = self.today_df.loc[i, "% by Market Cap"]
            price = self.today_df.loc[i, "Price (in Rs)"]
            quant = math.floor((((weight / 100) * beginning_capital) / price))
            self.today_df.loc[i, "Quantity"] = quant
            cash_spent += (price * quant)

        # cash_required = 0
        # for i in range(30):
        #     weight = self.today_df.loc[i, "% by Market Cap"]
        #     price = self.today_df.loc[i, "Price (in Rs)"]
        #     quant = self.today_df.floor((((weight / 100) * cash) / price))
        #     cash_required += quant * price
        #
        # if cash_required > cash:
        #     # The cash required to buy the required shares is less than that which is available
        #     print("Cash is Less -> Program has broken, Check")
        #     return

    def cash_check(self) -> bool:
        """Checks the capital which is required for rebalancing. Returns True, if the capital is available"""
        is_capital_available = False

        for i in range(30):
            quant_master = int(self.master_df.loc[i, "Quantity"])
            price_buy = self.master_df.loc[i, "Buy Price"]
            quant_today = int(self.today_df.loc[i, "Quantity"])
            price_today = self.today_df.loc[i, "Price (in Rs)"]
            buy_sell = quant_today - quant_master
            if buy_sell == 0:
                pass
            elif buy_sell > 0:
                # Buy
                self.buy[i] = abs(buy_sell * price_today)
                # i -> Index of the stock
                # buy_sell -> Amount Required to Buy the shares
            elif buy_sell < 0:
                # Sell
                profit_loss = (quant_today * price_today) \
                              - (quant_today * price_buy)
                if profit_loss <= 0:
                    # Loss or capital recovered
                    self.sell_loss[i] = abs(buy_sell * price_today)
                elif profit_loss > 0:
                    # Profit
                    profit = abs(profit_loss) * 0.15
                    capital = abs(buy_sell) * price_buy
                    self.sell_profit[i] = (profit + capital)

        total_cash_available = 0
        for key in self.sell_profit.keys():
            total_cash_available += self.sell_profit[key]
        for key in self.sell_loss.keys():
            total_cash_available += self.sell_loss[key]
        total_cash_available += self.cash

        total_cash_required = 0
        for key in self.buy.keys():
            total_cash_required += self.buy[key]

        if total_cash_available > total_cash_required:
            is_capital_available = True

        return is_capital_available

    def rebalance(self):
        """This re-balances our portfolio. It first sells the extra shares and then buys the deficit shares."""

        # Sell:
        for key in self.sell_profit.keys():
            description = f"Sell {self.master_df.loc[key, 'Ticker Symbol']} Shares"
            quant_req = self.today_df.loc[key, "Quantity"]
            self.master_df.loc[key, "Quantity"] = quant_req
            self.cash += self.sell_profit[key]
            self.ledger.credit(description, self.sell_profit[key])
        for key in self.sell_loss.keys():
            description = f"Sell {self.master_df.loc[key, 'Ticker Symbol']} Shares"
            quant_req = self.today_df.loc[key, "Quantity"]
            self.master_df.loc[key, "Quantity"] = quant_req
            self.cash += self.sell_loss[key]
            self.ledger.credit(description, self.sell_loss[key])

        # Buy:
        for key in self.buy.keys():
            # 2000 -> 100: 2,00,000 && 2200 -> 100: 2,20,000
            # Average Price = Total Price / Total Quant = (4,20,000)/200 = 2100
            description = f"Buy {self.master_df.loc[key, 'Ticker Symbol']} Shares"
            quant_master = self.master_df.loc[key, "Quantity"]
            quant_req = self.today_df.loc[key, "Quantity"]
            initial_total_price = quant_master * self.master_df.loc[key, "Buy Price"]
            buy_total_price = (quant_req - quant_master) * self.today_df.loc[key, "Price (in Rs)"]
            avg_buy_price = (initial_total_price + buy_total_price) / (self.today_df.loc[key, "Quantity"])
            self.master_df.loc[key, "Buy Price"] = avg_buy_price
            self.master_df.loc[key, "Quantity"] = quant_req
            self.cash -= self.buy[key]
            self.ledger.debit(description, self.buy[key])

    def master_updation(self):
        """Upadte 'Master DataFrame.csv' at the end of everyday"""
        for i in range(30):
            self.master_df.loc[i, "Price (in Rs)"] = self.today_df.loc[i, "Price (in Rs)"]
            self.master_df.loc[i, "FF Market Cap (in Cr)"] = self.today_df.loc[i, "FF Market Cap (in Cr)"]
            self.master_df.loc[i, "% by Market Cap"] = self.today_df.loc[i, "% by Market Cap"]

        self.master_df.to_csv('Master DataFrame.csv', index=False)
        self.ledger.save_cash_ledger()
