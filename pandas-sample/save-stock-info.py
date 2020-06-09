# fetch remove data to local excel: AAPL.xls/MSFT.xls
# https://github.com/pydata/pandas-datareader/blob/master/pandas_datareader/data.py
import datetime
import os
import pandas as pd
import pandas_datareader.data as web
import sys
import warnings


if not sys.warnoptions:
    warnings.simplefilter("ignore")
    warnings.filterwarnings("ignore", category=FutureWarning)
    print('use export PYTHONWARNINGS="ignore" to disable warning')

start = datetime.datetime(2018, 1, 1)
end = datetime.date.today()

if os.path.exists('data/AAPL.xls'):
    print('data/AAPL.xls exist')
else:
    apple = web.DataReader("AAPL", "yahoo", start, end)
    # pandas.core.frame.DataFrame
    print(f"type(apple)={type(apple)}")

stocks = ['AAPL', "GOOG", 'MSFT']
for stock in stocks:
    if os.path.exists(f'./data/{stock}.xls'):
        print(f'./data/{stock}.xls exist')
        continue
    # save to excel
    print(f"saving {stock}.xls ...")
    web.DataReader(stock, 'yahoo', start, end).to_excel(
        f'./data/{stock}.xls')

# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html
# index_col: int, default None. Column (0-indexed) to use as the row labels.
apple = pd.read_excel("./data/AAPL.xls", index_col=0)
ms = pd.read_excel("./data/MSFT.xls", index_col=0)

print(f"\n=== head of stock ===\n{apple.head()}\n")
print(f"\n=== index of stock ===\n{apple.index}\n")
print(f"=== apple.describe ===\n{apple.describe()}")
