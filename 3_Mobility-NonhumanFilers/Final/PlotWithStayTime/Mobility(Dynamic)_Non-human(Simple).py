import pandas as pd
import matplotlib.pyplot as plt

# Show full columns at print
pd.set_option('display.max_colwidth', None)
# Load data into a Pandas DataFrame
path = r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData\output'
df = pd.read_csv(path + "\Filtered.alk_data_23_02_19_to_23_04_03.csv")

# Convert Datetime column to datetime type
df['Datetime'] = pd.to_datetime(df['Datetime'])

# Sort by Datetime
df = df.sort_values('Datetime')

# Calculate time difference between consecutive records for each user
df['time_diff'] = df.groupby(['user'])['Datetime'].diff()

# Assign visit-IDs
df['visit_id'] = (df['time_diff'] > pd.Timedelta(hours=1)).cumsum()

# Calculate the stay time for each user on each floor per visit-ID
df['stay_time'] = df.groupby(['user', 'Corrected_Floor', 'visit_id'])['time_diff'].cumsum()

# Non-Human Filter: filter out records with stay times over 12 hours
filtered_data = df[df['stay_time'] <= pd.Timedelta(hours=12)]

# mobility lookup table as nested dictionary
mobility_lookup = {
    'Student': {1: 'High', 2: 'High', 3: 'Med', 4: 'Med', 5: 'Low', 6: 'Low', 7: 'Med'},
    'Staff': {1: 'Low', 2: 'Low', 3: 'Low', 4: 'Med', 5: 'High', 6: 'High', 7: 'Med'},
    'Guest': {1: 'High', 2: 'High', 3: 'High', 4: 'High', 5: 'High', 6: 'High', 7: 'Low'}
}

threshold_values = {'High': 5, 'Med': 10, 'Low': 15}

#function to get the mobility threshold based on Floor and vlan_role
def get_mobility_threshold(floor, vlan_role):
    threshold_key = mobility_lookup.get(vlan_role, {}).get(floor, 'High')
    return pd.Timedelta(minutes=threshold_values[threshold_key])

# apply function to store new mobility threshold
filtered_data = filtered_data[filtered_data.apply(lambda row: row['stay_time'] >= get_mobility_threshold(row['Corrected_Floor'], row['vlan_role']), axis=1)]

# Group by user, floor, and visit_id, and keep only the first connection time for each visit
filtered_data = filtered_data.groupby(['user', 'Corrected_Floor', 'visit_id'], as_index=False).agg({
    'stay_time': 'max',
    'Datetime': 'min',
    'vlan_role': 'first'
})

# Sort by user and Datetime
filtered_data = filtered_data.sort_values(['user', 'Datetime'])

# Export to csv
filtered_data.to_csv(path + r'\Mobility(Dynamic)_Non-humanFilter.csv')

################################Plotting##############################################

# Find the unique floors in the filtered_data and sort them
unique_floors = sorted(filtered_data['Corrected_Floor'].unique())

# Create a line plot for each floor's occupancy and an additional plot for total daily visits
fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, figsize=(10, 18), sharex=True)


# Plot the occupancy for each floor
for floor in unique_floors:
    floor_data = filtered_data[filtered_data['Corrected_Floor'] == floor]
    floor_occupancy = floor_data.groupby([pd.Grouper(key='Datetime', freq='60T')])['user'].nunique()
    floor_occupancy.plot(ax=ax1, label=f'Floor {floor}')

# Customize the first plot
ax1.set_ylabel("Number of Users")
ax1.set_title("Floor Occupancy: Dynamic Filters (1-hour intervals)")
ax1.legend(loc='upper right')

# Calculate and plot the total daily visits for all floors
total_daily_visits = filtered_data.groupby(pd.Grouper(key='Datetime', freq='D'))['user'].count()
total_daily_visits.plot(ax=ax2, marker='o')

# Customize the second plot
ax2.set_ylabel("Total Visits")
ax2.set_xlabel("Datetime")
ax2.set_title("Total Daily Visits")

# Calculate and plot the total unique daily visits for all floors
unique_daily_visits = filtered_data.groupby(['user', pd.Grouper(key='Datetime', freq='D')]).size().reset_index().groupby(pd.Grouper(key='Datetime', freq='D'))['user'].count()
unique_daily_visits.plot(ax=ax3, marker='o')

# Customize the third plot
ax3.set_ylabel("Unique Visits")
ax3.set_xlabel("Datetime")
ax3.set_title("Total Unique Daily Visits")


# Show the plots
plt.tight_layout()
plt.show()
