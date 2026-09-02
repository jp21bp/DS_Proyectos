"""
This file details the data collection process using YFinance APIs
"""


##### Importing libraries
import yfinance as yf
import os

##### Directory path
data_path = os.path.join(
    os.getcwd(),
    '2_OptimizacionPortafolio'
)

#######################################################################
    # SPLAC index #
##### Getting the ticker
splac_tick =  yf.Ticker("^SPLAC")

##### Download and Collection
start_date = "2000-07-30"
    #Launch data = September 30, 1999
end_date = "2026-07-31"
    #Top 40 recorded on 7/31/26
df_splac_raw = splac_tick.history(interval='1d', start = end_date, end=end_date)

##### SAve only 'Adj Close'
df_splac_AC = df_splac_raw.xs('Adj Close', axis=1, level=0)
df_splac_AC.to_csv(f'{data_path}/Data/raw_splac.csv', index=True, encoding='utf-8')

##### Alternative, if above doesn't work
    # Go to Google Sheets and PLace the following command
    # =GOOGLEFINANCE("INDEXSP:SPLAC", "price", "2000-01-01", "2026-07-31", "DAILY")

#######################################################################
    # Top 40 Inside SPLAC #
##### Tickers
with open(f'{data_path}/SPLAC_tickers.txt', 'r', encoding='utf-8') as file:
    tickers = file.readlines()
tickers = sorted([elem.rstrip('\n') for elem in tickers])


##### Download and Collection
start_date = "2000-01-01"
    #Launch data = September 30, 1999
end_date = "2026-07-31"
    #Top 40 recorded on 7/31/26
df_raw = yf.download(tickers, start=start_date, end=end_date, auto_adjust=False)

##### Filter to only save 'Adj Close' and dates
df_raw_AC = df_raw.xs('Adj Close', axis=1, level=0)
df_raw_AC.to_csv(f'{data_path}/Data/raw_top40.csv', index=True, encoding='utf-8')