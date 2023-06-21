import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
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

# Initialize 'Count' column
GroundTruth['StaticCount'] = 0

# Count unique users for each row in GroundTruth
for idx, row in GroundTruth.iterrows():
    GroundTruth.loc[idx, 'StaticCount'] = WifiStatic[(WifiStatic['Datetime'] <= row['Median_Time']) &
                                (row['Median_Time'] < WifiStatic['end_time']) &
                                (WifiStatic['Corrected_Floor'] == row['Floor'])]['user'].nunique()

GroundTruth = GroundTruth.sort_values(by='Median_Time')

floors = sorted(GroundTruth['Floor'].unique())  # Sort floor values

# Set font family to Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'

# Define markers and colors
markers = ['o', 's', 'v', 'p', '*', 'H', 'D', 'd', 'P', 'X', '^', '<', '>']
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

plt.figure(figsize=(15, 10))

for i, floor in enumerate(floors):
    subset = GroundTruth[GroundTruth['Floor'] == floor]
    plt.plot(subset['Median_Time'], subset['MedianTotal'], marker=markers[i], linestyle='-', color=colors[i % len(colors)], label=f'Floor {floor} Ground Truth')
    plt.plot(subset['Median_Time'], subset['StaticCount'], marker=markers[i], linestyle='--', color=colors[i % len(colors)], label=f'Floor {floor} Wi-Fi Static')

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.gca().xaxis.set_major_locator(mdates.HourLocator())

plt.title('Comparison of Ground Truth and Static Wi-Fi counts Over Time', fontsize=19, fontname='Times New Roman')
plt.xlabel('Time', fontsize=16, fontname='Times New Roman')
plt.ylabel('Values', fontsize=16, fontname='Times New Roman')

plt.legend(loc='upper right', fontsize=13)

plt.xticks(fontsize=14, fontname='Times New Roman')
plt.yticks(fontsize=14, fontname='Times New Roman')

plt.tight_layout()
plt.grid(True)

plt.savefig('comparison_plot.png', dpi=300)
plt.show()

# Calculate Mean Absolute Percentage Error (MAPE) for each floor
floors = range(3, 8)
mape_results = []

for floor in floors:
    subset = GroundTruth[GroundTruth['Floor'] == floor]
    actual_values = subset['MedianTotal']
    predicted_values = subset['StaticCount']
    mape = (abs(predicted_values - actual_values) / actual_values).mean() * 100
    mape_results.append(mape)

# Print MAPE results
for floor, mape in zip(floors, mape_results):
    print(f'Floor {floor} MAPE: {mape:.2f}%')

# Convert 'Median_Time' to datetime if necessary
GroundTruth['Median_Time'] = pd.to_datetime(GroundTruth['Median_Time'])

# Plot bar graphs
plt.figure(figsize=(15, 10))
plt.suptitle('Comparison Between Ground Truth and Static Wi-Fi Counts By Floor', fontsize=18, fontname='Times New Roman')

bar_width = 0.35

for i, floor in enumerate(floors):
    subset = GroundTruth[GroundTruth['Floor'] == floor]
    index = range(len(subset))

    plt.subplot(2, 3, i + 1)
    ground_truth_bar = plt.bar(index, subset['MedianTotal'], width=bar_width, label='Ground Truth Count')
    Static_wifi_bar = plt.bar([j + bar_width for j in index], subset['StaticCount'], width=bar_width,
                              label='Static Wi-Fi Count')

    # Calculate MAPE
    mape = abs((subset['StaticCount'] - subset['MedianTotal']) / subset['MedianTotal']) * 100
    mape_label = f'MAPE: {mape.mean():.2f}%'

    plt.xticks(index, subset['Median_Time'].dt.strftime('%H:%M'), rotation=45, ha='right', fontsize=16)
    plt.yticks(fontsize=16)

    plt.title(f'Floor {floor} - {mape_label}', fontsize=17, fontname='Times New Roman')

    if i == 0:
        plt.legend(loc='best', prop={'size': 13})
        plt.xlabel('Time', fontsize=15, fontname='Times New Roman')
        plt.ylabel('Count', fontsize=15, fontname='Times New Roman')
    plt.grid()

plt.tight_layout()
plt.show()