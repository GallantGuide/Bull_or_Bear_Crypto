import pandas as pd
import time

from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager

def get_historical_data(browser, ticker, start, end):
    """Given a list of crypto tickers and a start and end data (format = ‘mm/dd/yyyy’) return the historical price data from Yahoo Finance."""

    #Define helper functions
    def create_epoch(date):
        """Given data (format = ‘mm/dd/yyyy’) return the Epoch."""
        date_time = f"{date} 12:59:59"
        pattern = '%m/%d/%Y %H:%M:%S'
        return int(time.mktime(time.strptime(date_time, pattern)))


    def parse_html(fin_soup):
        """Given html data from Yahoo Finance return a price history dataframe."""

        # Parse out the rows
        rows = []
        for section in fin_soup.find('table').children:
            for tr in section:
                row = []
                for tx in tr:
                    row.append(tx.text)
                rows.append(row)

        # make dataframe
        return pd.DataFrame(rows[1:len(rows) - 1], columns = rows[0])



    # Execute code
    final_df = pd.DataFrame()

    # get the base URL and UNIX date ranges
    base_url = 'https://finance.yahoo.com/quote/'
    start = create_epoch(start) - 86400
    end = create_epoch(end)
    days_100 = 86400 * 100

    # get info in chunks of 100 because of how YF loads
    while start < end:

        # get 100 days past the start as the end
        current_end = end if start + days_100 > end else start + days_100

        # visit website and prase out data
        url = f"{base_url}{ticker}/history?period1={start}&period2={current_end}"
        browser.visit(url)
        html = browser.html
        df = parse_html(bs(html, 'html.parser'))

        # add data to final df and make the current end_date next start date 
        final_df = final_df.append(df)
        start = current_end

    # final df cleaning
    final_df['Date'] = pd.to_datetime(final_df['Date'])
    final_df = final_df.sort_values(by = 'Date')

    return final_df.reset_index(drop = True)
