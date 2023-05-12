"""
Description:
This script processes Wi-Fi access data to aggregate the number of unique users by role (Guest, Staff, Student) for each
hourly interval and outputs the results in a CSV file. Additionally, it generates a plot of the total number of users over time.
"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# Read the CSV file
path = r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData\output'
filtered_data = pd.read_csv(os.path.join(path, 'Mobility(Static)_Non-humanFilter.csv'))

# Convert Datetime column to datetime type
filtered_data['Datetime'] = pd.to_datetime(filtered_data['Datetime'])

# Convert stay_time to timedelta type
filtered_data['stay_time'] = pd.to_timedelta(filtered_data['stay_time'])

# Round Datetime to the nearest hour
filtered_data['Datetime'] = filtered_data['Datetime'].dt.round('60min')

# Calculate the EndDatetime
filtered_data['EndDatetime'] = filtered_data['Datetime'] + filtered_data['stay_time']

# Create empty DataFrame to store the final results
results = []

# Loop through unique dates and floors
unique_dates = filtered_data['Datetime'].dt.date.unique()
unique_floors = filtered_data['Corrected_Floor'].unique()

for date in unique_dates:
    for floor in unique_floors:
        # Filter the data for the current date and floor
        data = filtered_data[(filtered_data['Datetime'].dt.date == date) & (filtered_data['Corrected_Floor'] == floor)]

        if data.empty:
            continue

        # Create hourly intervals for the current date
        start_time = data['Datetime'].min().replace(minute=0, second=0)
        end_time = data['Datetime'].max().replace(minute=0, second=0) + pd.Timedelta(hours=1)
        intervals = pd.date_range(start=start_time, end=end_time, freq='H')

        for i in range(len(intervals) - 1):
            start_interval = intervals[i]
            end_interval = intervals[i + 1]

            # Filter the data for the current interval
            data_interval = data[((data['Datetime'] >= start_interval) & (data['Datetime'] < end_interval)) |
                                 ((data['EndDatetime'] > start_interval) & (data['EndDatetime'] <= end_interval)) |
                                 ((data['Datetime'] < start_interval) & (data['EndDatetime'] > end_interval))]

            # Count unique users for each role
            unique_guests = data_interval[data_interval['vlan_role'] == 'Guest']['user'].nunique()
            unique_staff = data_interval[data_interval['vlan_role'] == 'Staff']['user'].nunique()
            unique_students = data_interval[data_interval['vlan_role'] == 'Student']['user'].nunique()

            # Append the result to the results list
            results.append([start_interval, floor, unique_guests, unique_staff, unique_students, unique_guests + unique_staff + unique_students])

# Create a DataFrame from the results list
columns = ['Datetime', 'Corrected_Floor', 'Guest', 'Staff', 'Student', 'Total']
aggregated_data = pd.DataFrame(results, columns=columns)

# Group by Datetime and sum the counts for all floors
building_totals = aggregated_data.groupby('Datetime').sum().reset_index().drop(columns=["Corrected_Floor"])

# Save the DataFrame to a CSV file
building_totals.to_csv(os.path.join(path, r'agg\aggDuration\BuildingCounts_60min_static.csv'), index=False)

# Create a plot
fig, ax = plt.subplots(figsize=(15, 6))
ax.plot(building_totals['Datetime'], building_totals['Total'], label='Building Total')

# Format the x-axis
ax.set_xlabel('Datetime')
ax.xaxis.set_major_locator(plt.MaxNLocator(20))
plt.xticks(rotation=45)

# Format the y-axis
ax.set_ylabel('Total Count')

# Add a legend and title
ax.legend()
ax.set_title('Counts of Building Total at Every 1-hour Interval: Static Filter')

# Show the plot
plt.tight_layout()
plt.show()