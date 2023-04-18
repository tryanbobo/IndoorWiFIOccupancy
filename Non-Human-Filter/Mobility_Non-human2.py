import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# show full columns at print
pd.set_option('display.max_colwidth', None)
# load data into a Pandas DataFrame
path = r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData\output'
df = pd.read_csv(path + "\Preprocessed.alk_data_23_02_19_to_23_04_03.csv")

# Create sub-set to test data
df = df.head(100000)
# convert Datetime column to datetime type
df['Datetime'] = pd.to_datetime(df['Datetime'])

# sort by Datetime
df = df.sort_values('Datetime')

# calculate time difference between consecutive records for each user and floor
df['time_diff'] = df.groupby(['user', 'Floor'])['Datetime'].diff()
print(df)


def generate_visit_id(time_diff_series):
    visit_id = pd.Series(np.zeros(len(time_diff_series), dtype=int), index=time_diff_series.index)
    current_visit_id = 1

    for i in range(1, len(time_diff_series)):
        if pd.isna(time_diff_series.iloc[i]) or time_diff_series.iloc[i] >= pd.Timedelta(hours=4):
            current_visit_id += 1
        visit_id[i] = current_visit_id

    return visit_id


# Apply the custom function to create the 'visit_id' column
df['visit_id'] = 0
for _, group in df.groupby(['user', 'Floor']):
    group_index = group.index
    visit_id = generate_visit_id(group['time_diff'])
    df.loc[group_index, 'visit_id'] = visit_id
print(df)
# calculate the stay time for each user on each floor per visit
df['stay_time'] = df.groupby(['user', 'Floor', 'visit_id'])['time_diff'].cumsum()

#calculate the daily stay time for each user
df['daily_stay_time'] = df.groupby(['user', pd.Grouper(key='Datetime', freq='24H')])['stay_time'].transform('sum')


####################Check distribution before filters########################
# Plot histogram of time differences
time_diff_minutes = df['time_diff'].dt.total_seconds() / 60
time_diff_minutes.plot.hist(bins=100, log=True)
plt.xlabel('Time difference (minutes)')
plt.title('Histogram of time differences between consecutive records')
plt.show()


# Non-Human Filter: filter out records where total stay time is greater than 12 hours
df = df[df['daily_stay_time'] < pd.Timedelta(hours=12)]
print('After Non-Human Filter: ',len(df))

# Mobility Filter: filter out records where stay time is less than 5 minutes
df = df[df['stay_time'] >= pd.Timedelta(minutes=5)]
print('After Mobility Filter: ',len(df))
# group by user and floor, and keep only the first connection time for each visit
filtered_data = df.groupby(['user', 'Floor', 'visit_id'], as_index=False).agg({
    'stay_time': 'max',
    'Datetime': 'min',
    'vlan_role': 'first'
})

# sort by user and Datetime
filtered_data = filtered_data.sort_values(['user', 'Datetime'])

# export to csv
filtered_data.to_csv(path + r'\Mobility_Non-humanFilter.csv')

print(filtered_data.head())
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
total_daily_visits = filtered_data.groupby([pd.Grouper(key='Datetime', freq='D')])['user'].count()
if not total_daily_visits.empty:
    total_daily_visits.plot(ax=ax2, linestyle='-', marker='o', linewidth=2)
else:
    print("No data to plot for total daily visits.")

# Customize the second plot
ax2.set_ylabel("Number of Users")
ax2.set_title("Total Daily Visits")

# Set the x-axis label for both plots
fig.text(0.5, 0.04, 'Date', ha='center', va='center')


# Display the plots
# Check if the filtered_data DataFrame is empty
if not filtered_data.empty:
    # Display the plots
    plt.show()
else:
    print("No data to plot after applying the filters.")

