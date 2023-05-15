import pandas as pd

pd.set_option('display.max_columns', None)

# Load CSV files
WifiStatic = pd.read_csv(r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData\output\Mobility(Static)_Non-humanFilter.csv')
GroundTruth = pd.read_csv(r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\GroundTruth\GroundTruth-03-02-2023_Simple.csv')

# Convert 'Datetime' and 'stay_time' to datetime and timedelta objects respectively
WifiStatic['Datetime'] = pd.to_datetime(WifiStatic['Datetime'])
WifiStatic['Datetime'] = WifiStatic['Datetime'].dt.tz_convert('US/Central').dt.tz_localize(None)
WifiStatic['stay_time'] = pd.to_timedelta(WifiStatic['stay_time'])

# Calculate 'end_time'
WifiStatic['end_time'] = WifiStatic['Datetime'] + WifiStatic['stay_time']

# Convert 'Median_Time' to datetime object and floor to nearest minute
GroundTruth['Median_Time'] = pd.to_datetime(GroundTruth['Median_Time']).dt.floor('Min')
print(GroundTruth)
# Initialize 'Count' column
GroundTruth['StaticCount'] = 0

# Count unique users for each row in GroundTruth
for idx, row in GroundTruth.iterrows():
    GroundTruth.loc[idx, 'StaticCount'] = WifiStatic[(WifiStatic['Datetime'] <= row['Median_Time']) &
                                (row['Median_Time'] < WifiStatic['end_time']) &
                                (WifiStatic['Corrected_Floor'] == row['Floor'])]['user'].nunique()

# Save GroundTruth to a new CSV file
GroundTruth.to_csv(r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData\output\RQ2\GT-StaticWifi.csv', index=False)

print(filtered)
print(WifiStatic)