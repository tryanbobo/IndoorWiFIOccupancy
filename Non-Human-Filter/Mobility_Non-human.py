import pandas as pd
import matplotlib.pyplot as plt


# load data into a Pandas DataFrame
path = r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData\output'
df = pd.read_csv(path + "\Preprocessed.alk_data_23_02_19_to_23_04_03.csv")

# convert Datetime column to datetime type
df['Datetime'] = pd.to_datetime(df['Datetime'])

# sort by Datetime
df = df.sort_values('Datetime')

# calculate time difference between consecutive records for each user and floor
df['time_diff'] = df.groupby(['user', 'Floor'])['Datetime'].diff()


# filter out records where time difference is greater than 1 hour
df = df[df['time_diff'] < pd.Timedelta(hours=1)]

# calculate the stay time for each user on each floor per visit
df['stay_time'] = df.groupby(['user', 'Floor'])['time_diff'].cumsum()

# filter out records where stay time is less than 5 minutes
df = df[df['stay_time'] >= pd.Timedelta(minutes=5)]

# group by user and floor, and keep only the first connection time for each visit
filtered_data = df.groupby(['user', 'Floor'], as_index=False).agg({
    'stay_time': 'max',
    'Datetime': 'min'
})

# calculate the total stay time for each user on each floor
filtered_data['total_stay_time'] = filtered_data.groupby('user')['stay_time'].transform('sum')

# filter out records where total stay time is greater than 12 hours
filtered_data = filtered_data[filtered_data['total_stay_time'] < pd.Timedelta(hours=12)]

# sort by user and Datetime
filtered_data = filtered_data.sort_values(['user', 'Datetime'])

# export to csv
filtered_data.to_csv(path + r'\Mobility_Non-humanFilter.csv')

floor_occupancy = filtered_data[filtered_data['Floor'] == 1].groupby([pd.Grouper(key='Datetime', freq='H')])[
    'user'].count()
print(floor_occupancy)


# plot the data
floor_occupancy.plot(kind='line', figsize=(10,6))

# Set the plot title and axis labels
plt.title('Hourly Occupancy of the First Floor')
plt.xlabel('Hour of the Day')
plt.ylabel('Number of Occupants')

# Show the plot
plt.show()