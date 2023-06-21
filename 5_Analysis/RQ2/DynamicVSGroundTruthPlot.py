import pandas as pd
import seaborn as sns
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
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

GroundTruth = GroundTruth.sort_values(by='Median_Time')
# Save GroundTruth to a new CSV file
GroundTruth.to_csv(r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\Analysis\RQ2_\GT-DynamicWifi.csv', index=False)




# Convert 'Median_Time' to datetime if necessary
GroundTruth['Median_Time'] = pd.to_datetime(GroundTruth['Median_Time'])

floors = GroundTruth['Floor'].unique()

# Define markers and colors
markers = ['o', 's', 'v', 'p', '*', 'H', 'D', 'd', 'P', 'X', '^', '<', '>']
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

plt.figure(figsize=(15,10))

for i, floor in enumerate(floors):
    subset = GroundTruth[GroundTruth['Floor'] == floor]
    plt.plot(subset['Median_Time'], subset['MedianTotal'], marker=markers[i], linestyle='-', color=colors[i%len(colors)], label=f'Floor {floor} Ground Truth')
    plt.plot(subset['Median_Time'], subset['DynamicCount'], marker=markers[i], linestyle='--', color=colors[i%len(colors)], label=f'Floor {floor} Wi-Fi Dynamic')

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.gca().xaxis.set_major_locator(mdates.HourLocator())

plt.title('Comparison of MedianTotal and DynamicCount over time')
plt.xlabel('Median Time')
plt.ylabel('Values')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.subplots_adjust(left=0.06, bottom=0.084, right=0.785, top=0.94, wspace=0.2, hspace=0.196)
plt.grid()
plt.show()

