import pandas as pd
from scipy.stats import wilcoxon

# Read the occupancy and ground truth CSV files
occupancy_df = pd.read_csv(r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData\output\Mobility(Static)_Non-humanFilter.csv')
ground_truth_df = pd.read_csv(r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\GroundTruth\GroundTruth-03-02-2023_Simple.csv')

# Convert date and time columns to datetime objects
occupancy_df['Datetime'] = pd.to_datetime(occupancy_df['Datetime'])
ground_truth_df['Median_Time'] = pd.to_datetime(ground_truth_df['Median_Time'])

# Convert to timezone-naive datetime objects
occupancy_df['Datetime'] = occupancy_df['Datetime'].dt.tz_convert('US/Central').dt.tz_localize(None)

# Convert stay_time column to timedelta objects
occupancy_df['stay_time'] = pd.to_timedelta(occupancy_df['stay_time'])

# Add SnapShotWifiCount and Agg30WifiCount columns to the ground truth dataframe
ground_truth_df['SnapShotWifiCount'] = 0
ground_truth_df['Agg30WifiCount'] = 0

# Iterate through each row in the ground truth dataframe
for index, row in ground_truth_df.iterrows():
    floor = row['Floor']
    median_time = row['Median_Time']

    # Calculate SnapShotWifiCount
    snapshot_count = occupancy_df[
        (occupancy_df['Corrected_Floor'] == floor)
        & (occupancy_df['Datetime'] <= median_time)
        & (occupancy_df['Datetime'] + occupancy_df['stay_time'] >= median_time)
    ].shape[0]
    ground_truth_df.at[index, 'SnapShotWifiCount'] = snapshot_count

    # Calculate Agg30WifiCount
    start_time = median_time - pd.Timedelta(minutes=30)
    end_time = median_time + pd.Timedelta(minutes=29, seconds=59)
    agg_30min_count = occupancy_df[
        (occupancy_df['Corrected_Floor'] == floor)
        & (occupancy_df['Datetime'] + occupancy_df['stay_time'] >= start_time)
        & (occupancy_df['Datetime'] <= end_time)
    ].shape[0]
    ground_truth_df.at[index, 'Agg30WifiCount'] = agg_30min_count

# Write the updated ground truth dataframe to a new CSV file
ground_truth_df.to_csv(r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData\output\updated_ground_truth.csv', index=False)
print(ground_truth_df)

print('Wilcoxon test between ground truth and 30 minute aggregations')
print(wilcoxon(ground_truth_df['Agg30WifiCount'], ground_truth_df['MedianTotal']))

print('Wilcoxon test between ground truth and snap-shot time')
print(wilcoxon(ground_truth_df['SnapShotWifiCount'], ground_truth_df['MedianTotal']))
