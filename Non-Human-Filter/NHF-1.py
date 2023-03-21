import pandas as pd

# read the data from CSV file
path = r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData'
df = pd.read_csv(path + r'\alk_data_23_02_19_to_23_03_03.preprocessed.csv')

# define the duration threshold in seconds
duration_threshold = 12*60*60 # 12 hours in seconds

# define the gap threshold in seconds
gap_threshold = 30*60 # 30 minutes in seconds

# convert the 'Datetime' column to pandas datetime format
df['Datetime'] = pd.to_datetime(df['Datetime'])

# sort the data by 'user' and 'Datetime' columns
df.sort_values(['user', 'Datetime'], inplace=True)

# group the data by 'user' and 'Floor' columns
groups = df.groupby(['user', 'Floor'])

# create an empty list to store the filtered data
filtered_data = []

# loop over the groups
for name, group in groups:

    # calculate the duration of the group
    duration = (group.iloc[-1]['Datetime'] - group.iloc[0]['Datetime']).total_seconds()

    # calculate the maximum gap in the group
    gaps = group['Datetime'].diff().fillna(pd.Timedelta(seconds=0))
    max_gap = gaps.max().total_seconds()

    # check if the duration and gap are within the thresholds
    if duration <= duration_threshold and max_gap <= gap_threshold:

        # if the group passes the filters, add it to the filtered data
        filtered_data.append(group)

# concatenate the filtered data into a single dataframe
filtered_df = pd.concat(filtered_data)



# print the result
print(filtered_df)

# export to csv
df.to_csv(path + r'\output\non-humanFilter.csv')


df['timestamp_rounded'] = df['Datetime'].dt.floor('30T')
users_per_floor = df.groupby(['Floor', 'timestamp_rounded'])['User'].nunique()

print(df)