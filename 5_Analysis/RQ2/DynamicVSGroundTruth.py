import pandas as pd

pd.set_option('display.max_columns', None)

# Load CSV files
WifiDynamic = pd.read_csv(r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData\output\Mobility(Dynamic)_Non-humanFilter.csv')
GroundTruth = pd.read_csv(r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\GroundTruth\GroundTruth-03-02-2023_Simple.csv')

# Convert 'Datetime' and 'stay_time' to datetime and timedelta objects respectively
WifiDynamic['Datetime'] = pd.to_datetime(WifiDynamic['Datetime'])
WifiDynamic['Datetime'] = WifiDynamic['Datetime'].dt.tz_convert('US/Central').dt.tz_localize(None)
WifiDynamic['stay_time'] = pd.to_timedelta(WifiDynamic['stay_time'])

# Calculate 'end_time'
WifiDynamic['end_time'] = WifiDynamic['Datetime'] + WifiDynamic['stay_time']

# Convert 'Median_Time' to datetime object and floor to nearest minute
GroundTruth['Median_Time'] = pd.to_datetime(GroundTruth['Median_Time']).dt.floor('Min')
print(GroundTruth)
# Initialize 'Count' column
GroundTruth['DynamicCount'] = 0

# Count unique users for each row in GroundTruth
for idx, row in GroundTruth.iterrows():
    GroundTruth.loc[idx, 'DynamicCount'] = WifiDynamic[(WifiDynamic['Datetime'] <= row['Median_Time']) &
                                (row['Median_Time'] < WifiDynamic['end_time']) &
                                (WifiDynamic['Corrected_Floor'] == row['Floor'])]['user'].nunique()

# Save GroundTruth to a new CSV file
GroundTruth.to_csv(r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData\output\RQ2\GT-DynamicWifi.csv', index=False)


print(WifiDynamic)