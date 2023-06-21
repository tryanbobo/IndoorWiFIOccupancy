import pandas as pd
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
#GroundTruth = GroundTruth.sort_values(by='Median_Time')

GroundTruth = GroundTruth.sort_values(['Floor', 'Median_Time'])

floors = GroundTruth['Floor'].unique()
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'purple']

bar_width = 0.35
opacity = 0.8

fig, ax = plt.subplots(figsize=(15, 10))

# the number of bar pairs is equal to the number of unique 'Median_Time' values
unique_times = GroundTruth['Median_Time'].unique()
N = len(unique_times)
ind = np.arange(N)

for i, floor in enumerate(floors):
    counts_median_total = []
    counts_dynamic_count = []

    for time in unique_times:
        row = GroundTruth[(GroundTruth['Floor'] == floor) & (GroundTruth['Median_Time'] == time)]
        if row.empty:
            counts_median_total.append(0)
            counts_dynamic_count.append(0)
        else:
            counts_median_total.append(row['MedianTotal'].values[0])
            counts_dynamic_count.append(row['DynamicCount'].values[0])

    rects1 = ax.bar(ind - bar_width / 2 + i * bar_width, counts_median_total, bar_width,
                    alpha=opacity, color=colors[i], label=f'Floor {floor} MedianTotal')
    rects2 = ax.bar(ind + bar_width / 2 + i * bar_width, counts_dynamic_count, bar_width,
                    alpha=opacity, color=colors[i], label=f'Floor {floor} DynamicCount', hatch='//')

ax.set_xlabel('Median Time')
ax.set_ylabel('Counts')
ax.set_title(f'Counts by floor and time on {pd.Timestamp(unique_times[0]).strftime("%m/%d/%Y")}')
ax.set_xticks(ind)
ax.set_xticklabels([pd.Timestamp(time).strftime('%H:%M') for time in unique_times], rotation=45)
ax.legend()

plt.tight_layout()
plt.show()