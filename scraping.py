from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time


class Scraper:
    def __init__(self):
        opts = Options()
        opts.headless = True
        chrome_driver = "/Users/prannay/Google Drive/Computer Science/chromedriver"
        self.driver = webdriver.Chrome(executable_path=chrome_driver, options=opts)

    def bse_sensex_list(self) -> list:
        """Returns a list which contains the 30 stocks in Sensex 30."""
        
        self.driver.get("https://www.bseindia.com/sensex/code/16")
        soup = BeautifulSoup(self.driver.page_source, "lxml")

        sensex_list = []
        mainDiv_contents = soup.find(id="mainDiv").contents[0].contents[0]
        for tr in mainDiv_contents:
            try:
                for td in tr.contents:
                    try:
                        stock = td.contents[0].contents[0].contents[0].contents[0].string.strip()
                        sensex_list.append(stock)
                    except AttributeError:
                        continue
            except AttributeError:
                continue

        sensex_list = sensex_list[:30]
        return sensex_list

    def stock_scraper(self, stock: str) -> dict:
        """Parameter: Ticker Symbol
        Returns a dictionary with keys: name, ticker_symbol, price, ff_market_cap."""

        self.driver.get(f"https://www.screener.in/company/{stock}/consolidated/")
        time.sleep(1)
        bse_website_link = self.driver.find_element_by_xpath('//*[@id="top"]/div[2]/a[2]').get_attribute('href')
        return self.bse_stock_page_scraper(bse_website_link)

    def bse_stock_page_scraper(self, website_link: str) -> dict:
        """Scrapes the BSE Website of a particular stock and returns  stock_data_dict"""

        stock_data_dict = {
            "name": '',
            "ticker_symbol": '',
            "price": '',
            "ff_market_cap": '',  # Free Floating Market Cap
        }
        self.driver.get(website_link)
        while True:
            try:
                name = self.driver.find_element_by_xpath(
                    '//*[@id="getquoteheader"]/div[6]/div/div[3]/div/div[1]/div[1]/div[1]/div[2]/div/h1').text
                stock_data_dict["name"] = name.upper()
                ticker_symbol = self.driver.find_element_by_xpath(
                    '//*[@id="getquoteheader"]/div[6]/div/div[3]/div/div[1]/div[1]/div[1]/div[2]/div/div[2]')
                ticker_symbol = ticker_symbol.text.split("|")[0].strip()[1:]
                stock_data_dict["ticker_symbol"] = ticker_symbol
                price = float(self.driver.find_element_by_xpath('//*[@id="idcrval"]').text)
                stock_data_dict["price"] = price
                ff_market_cap = self.driver.find_element_by_xpath(
                    '//*[@id="getquoteheader"]/div[6]/div/div[4]/div/div[3]/div/table/tbody/tr[7]/td[2]')
                ff_market_cap = ff_market_cap.text  # In Crores
                # ff_market_cap = float(ff_market_cap.replace(",", "")) * 1000000000
                ff_market_cap = float(ff_market_cap.replace(",", ""))
                stock_data_dict["ff_market_cap"] = ff_market_cap
                break
            except:
                print(1)
                time.sleep(0.25)

        return stock_data_dict
