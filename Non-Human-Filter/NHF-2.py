import pandas as pd
from datetime import timedelta

# read in the data
path = r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData\output'
df = pd.read_csv(path + r'\Preprocessed.alk_data_23_02_19_to_23_04_03.csv')

# convert 'Datetime' column to datetime object and set as index
df['Datetime'] = pd.to_datetime(df['Datetime'])
df.set_index('Datetime', inplace=True)

# create a new dataframe with only the necessary columns
users = df[['user', 'Floor', 'AP_Name']].copy()

# drop duplicate rows and keep the first occurrence
users.drop_duplicates(subset=['user'], keep='first', inplace=True)

# group the users by their 'user' column and count the number of unique APs they have connected to
counts = users.groupby('user')['AP_Name'].nunique()

# filter out users who have connected to more than 1 AP and whose connection duration is greater than 12 hours
counts = counts[(counts == 1) & (users.groupby('user').apply(lambda x: x.index[-1] - x.index[0]) < timedelta(hours=12))]

# print the number of filtered users
print("Number of filtered users: ", len(counts))
# Print the total number of records and number of unique users
print("Total number of records:", len(df))
print("Number of unique users:", len(df['user'].unique()))

# Print the names and roles of the unique users
unique_users = df.drop_duplicates('user')[['user', 'Floor', 'vlan_role']]
print("Unique users:")
print(unique_users)





