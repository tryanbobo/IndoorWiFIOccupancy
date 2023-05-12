import pandas as pd
import matplotlib.pyplot as plt
import os

# Load and filter the data
path = r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData\output'
data = pd.read_csv(os.path.join(path, 'Mobility(Static)_Non-humanFilter.csv'))
data['Datetime'] = pd.to_datetime(data['Datetime'])
data['stay_time'] = pd.to_timedelta(data['stay_time'])
data['EndDatetime'] = data['Datetime'] + data['stay_time']

# Get unique dates, floors, and the timezone from the data
unique_dates = data['Datetime'].dt.date.unique()
unique_floors = data['Corrected_Floor'].unique()
timezone = data['Datetime'].iloc[0].tz

results = []

# Loop through each date and floor
for date in unique_dates:
    date = pd.Timestamp(date).tz_localize(timezone)
    for interval_start in pd.date_range(date, date + pd.DateOffset(days=1), freq='30min', closed='left'):
        interval_end = interval_start + pd.Timedelta(minutes=30)

        for floor in unique_floors:
            # Filter the data for the current date, floor, and interval
            data_interval = data[((data['Datetime'] >= interval_start) & (data['Datetime'] < interval_end)) |
                                 ((data['EndDatetime'] > interval_start) & (data['EndDatetime'] <= interval_end)) |
                                 ((data['Datetime'] < interval_start) & (data['EndDatetime'] > interval_end))]
            data_interval = data_interval[data_interval['Corrected_Floor'] == floor]

            # Calculate the counts
            guest_count = data_interval[data_interval['vlan_role'] == 'Guest']['vlan_role'].count()
            staff_count = data_interval[data_interval['vlan_role'] == 'Staff']['vlan_role'].count()
            student_count = data_interval[data_interval['vlan_role'] == 'Student']['vlan_role'].count()
            total_count = guest_count + staff_count + student_count

            results.append({
                'Datetime': interval_start,
                'Corrected_Floor': floor,
                'Guest': guest_count,
                'Staff': staff_count,
                'Student': student_count,
                'Total': total_count
            })

# Create a DataFrame from the results
results_df = pd.DataFrame(results)
# Sort the results DataFrame by 'Datetime' and 'Corrected_Floor'
results_df = results_df.sort_values(['Datetime', 'Corrected_Floor'])
results_df.to_csv(path + r"\agg\aggDuration\FloorCounts_30min_static.csv", index=False)

# sort the unique floor array
unique_floors = sorted(unique_floors)
# Plot the results
plt.figure(figsize=(15, 6))
for floor in unique_floors:
    plt.plot(results_df[results_df['Corrected_Floor'] == floor]['Datetime'], results_df[results_df['Corrected_Floor'] == floor]['Total'], label=f'Floor {floor}')

plt.legend()
plt.xlabel('Datetime')
plt.ylabel('Occupancy count')
plt.title('Occupancy count for each floor at 30-minute intervals: Static Filter')
plt.show()