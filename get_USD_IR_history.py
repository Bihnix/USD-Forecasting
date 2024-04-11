import pandas as pd 
import requests
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings('ignore')
import datetime

import time

current_unixtime = int(time.time())

datetime.datetime.fromtimestamp(current_unixtime)

print(datetime.datetime.fromtimestamp(current_unixtime))

print('Start:\n')
print(f"Date from {datetime.datetime.fromtimestamp(1262304000)} to {datetime.datetime.fromtimestamp(current_unixtime)}")

url = 'https://dashboard-api.tgju.org/v1/tv/history?symbol=PRICE_DOLLAR_RL&resolution=1D&from=1262304000&to=' + str(current_unixtime)
try:
    res = requests.get(url=url)
    res_j = res.json()
except requests.exceptions.RequestException as e:
    print(f"Error occurred during request: {e}")

# Get the column names from the dictionary
column_names = list(res_j.keys())

res_j.pop('s')
res_j.pop('v')

# Create the DataFrame
try:
  hisotry_raw = pd.DataFrame.from_dict(res_j)
except pd.errors.ParserError as e:
  print(f"Error occurred while parsing the data: {e}")

# Convert the unix timestamp column to datetime
try:
  hisotry_raw['t'] = pd.to_datetime(hisotry_raw['t'],unit='s')
except pd.errors.OutOfBoundsDatetime as e:
  print(f"Error occurred while converting the timestamp: {e}")

hisotry_raw.to_csv('hisotry_raw.csv', index=False)

print('history_raw saved.')

# Select the relevant columns
history_processed = hisotry_raw[['t','c']].copy()
# Rename the columns
history_processed.rename(columns={'t':'ds','c':'y'}, inplace= True)
# Filter the data to start from 2017-01-01
history_processed = history_processed[history_processed['ds'] >= '2012-01-01'].reset_index().drop(columns='index')
# Drop duplicates
history_processed = history_processed.drop_duplicates(subset=['ds'])

scaler = MinMaxScaler()
history_processed["y"] = scaler.fit_transform(history_processed["y"].values.reshape(-1, 1))

# Save the DataFrame to a CSV file
history_processed.to_csv('history_processed.csv', index=False)
print('history_processed saved.')

print(history_processed.head())
print(history_processed.tail())
print('Done.')