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
df_raw_AC.to_csv(f'{data_path}/Data/raw_splac.csv', index=True, encoding='utf-8')