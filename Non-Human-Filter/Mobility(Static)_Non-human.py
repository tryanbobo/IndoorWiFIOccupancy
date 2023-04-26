import pandas as pd
import matplotlib.pyplot as plt

# Show full columns at print
pd.set_option('display.max_colwidth', None)
# Load data into a Pandas DataFrame
path = r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData\output'
df = pd.read_csv(path + "\Preprocessed.alk_data_23_02_19_to_23_04_03.csv")

# Convert Datetime column to datetime type
df['Datetime'] = pd.to_datetime(df['Datetime'])

# Sort by Datetime
df = df.sort_values('Datetime')

# Calculate time difference between consecutive records for each user and floor
df['time_diff'] = df.groupby(['user', 'Floor'])['Datetime'].diff()

# Assign visit IDs
df['visit_id'] = (df['time_diff'] > pd.Timedelta(hours=1)).cumsum()

# Calculate the stay time for each user on each floor per visit
df['stay_time'] = df.groupby(['user', 'visit_id'])['time_diff'].cumsum()

# Non-Human Filter: filter out records where total stay time is greater than 12 hours
filtered_data = df.groupby(['user', pd.Grouper(key='Datetime', freq='24H')])['stay_time'].sum().reset_index()
filtered_data = filtered_data[filtered_data['stay_time'] < pd.Timedelta(hours=12)]
filtered_data = df[df['user'].isin(filtered_data['user'])]

# Mobility Filter: filter out records where stay time is less than 5 minutes
filtered_data = filtered_data[filtered_data['stay_time'] >= pd.Timedelta(minutes=5)]

# Group by user, floor, and visit_id, and keep only the first connection time for each visit
filtered_data = filtered_data.groupby(['user', 'Floor', 'visit_id'], as_index=False).agg({
    'stay_time': 'max',
    'Datetime': 'min',
    'vlan_role': 'first'
})

# Sort by user and Datetime
filtered_data = filtered_data.sort_values(['user', 'Datetime'])

# Export to csv
filtered_data.to_csv(path + r'\Mobility_Non-humanFilter.csv')

################################Plotting##############################################

# Find the unique floors in the filtered_data and sort them
unique_floors = sorted(filtered_data['Floor'].unique())

# Create a line plot for each floor's occupancy and an additional plot for total daily visits
fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, figsize=(10, 18), sharex=True)

# Plot the occupancy for each floor
for floor in unique_floors:
    floor_occupancy = filtered_data[filtered_data['Floor'] == floor].groupby(
        [pd.Grouper(key='Datetime', freq='30T')])['user'].count()
    floor_occupancy.plot(ax=ax1, label=f'Floor {floor}')

# Customize the first plot
ax1.set_ylabel("Number of Users")
ax1.set_title("Floor Occupancy (1-hour intervals)")
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
