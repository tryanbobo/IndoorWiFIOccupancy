import pandas as pd

# load data into a Pandas DataFrame
path = r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData\output'
df = pd.read_csv(path+"\Preprocessed.alk_data_23_02_19_to_23_04_03.csv")

# print row count
dfRowCount = len(df.index)

print('Total row count: ', dfRowCount)
# convert Datetime column to datetime data type
df['Datetime'] = pd.to_datetime(df['Datetime'])

# calculate time differences between consecutive connections for each user
df['time_diff'] = df.groupby('user')['Datetime'].diff()

# create a filtered DataFrame based on the conditions
filtered_data = df.groupby(['user', 'Floor'], as_index=False).agg({
    'time_diff': lambda x: ((x > pd.Timedelta(hours=1)).cumsum() * x < pd.Timedelta(hours=12)).any(),
    'Datetime': 'min'
})

# select only the rows where the time difference is True
filtered_data = filtered_data[filtered_data['time_diff']].drop(columns=['time_diff'])

# print length of non-human filter
filtered_dataRowCount = len(filtered_data.index)
print('New row count: ', filtered_dataRowCount)
print (dfRowCount - filtered_dataRowCount, ' rows were removed')
# display the filtered data
print(filtered_data.head())

#export to csv
filtered_data.to_csv(path + r'\Non-humanFilter.csv')