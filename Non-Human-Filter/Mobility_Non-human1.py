import pandas as pd
import matplotlib.pyplot as plt

# show full columns at print
pd.set_option('display.max_colwidth', None)
# load data into a Pandas DataFrame
path = r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData\output'
df = pd.read_csv(path + "\Preprocessed.alk_data_23_02_19_to_23_04_03.csv")

# convert Datetime column to datetime type
df['Datetime'] = pd.to_datetime(df['Datetime'])

# sort by Datetime
df = df.sort_values('Datetime')

# calculate time difference between consecutive records for each user and floor
df['time_diff'] = df.groupby(['user', 'Floor'])['Datetime'].diff()
print(df)

# filter out records where time difference is greater than 1 hour
df = df[df['time_diff'] < pd.Timedelta(hours=1)]

# calculate the stay time for each user on each floor per visit
df['stay_time'] = df.groupby(['user', 'Floor'])['time_diff'].cumsum()

# calculate the total stay time for each user on each floor
df['total_stay_time'] = df.groupby(['user', pd.Grouper(key='Datetime', freq='24H')])['stay_time'].transform('sum')

# Non-Human Filter: filter out records where total stay time is greater than 12 hours
df = df[df['total_stay_time'] < pd.Timedelta(hours=12)]

# Mobility Filter: filter out records where stay time is less than 5 minutes
df = df[df['stay_time'] >= pd.Timedelta(minutes=5)]

# group by user and floor, and keep only the first connection time for each visit
filtered_data = df.groupby(['user', 'Floor'], as_index=False).agg({
    'stay_time': 'max',
    'Datetime': 'min',
    'vlan_role': 'first'
})

# sort by user and Datetime
filtered_data = filtered_data.sort_values(['user', 'Datetime'])

# export to csv
filtered_data.to_csv(path + r'\Mobility_Non-humanFilter.csv')


## note: freq='H' for and hour; freq='30T' for 30-min
#floor_occupancy = filtered_data[filtered_data['Floor'] == 4].groupby([pd.Grouper(key='Datetime', freq='H')])[
#    'user'].count()
#print(floor_occupancy)


################################Plotting##############################################

# Find the unique floors in the filtered_data and sort them
unique_floors = sorted(filtered_data['Floor'].unique())

# Create a line plot for each floor's occupancy and an additional plot for total daily visits
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(10, 12), sharex=True)


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

# Show the plots
plt.tight_layout()
plt.show()
"""
#Plots each floors occupancy counts per hour
# plot the data for each floor
# Find the unique floors in the filtered_data
unique_floors = sorted(filtered_data['Floor'].unique())

# Create a line plot for each floor's occupancy
fig, ax = plt.subplots(figsize=(10, 6))

for floor in unique_floors:
    floor_occupancy = filtered_data[filtered_data['Floor'] == floor].groupby(
        [pd.Grouper(key='Datetime', freq='30T')])['user'].count()
    floor_occupancy.plot(ax=ax, label=f'Floor {floor}')

# Customize the plot
ax.set_ylabel("Number of Users")
ax.set_xlabel("Datetime")
ax.set_title("Floor Occupancy (30-minute intervals)")
ax.legend(loc='upper right')

# Show the plot
plt.show()
"""
