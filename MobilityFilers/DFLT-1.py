# Load data
import pandas as pd

path = r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData'
df = pd.read_csv(path + r'\alk_data_23_02_19_to_23_03_03.preprocessed.csv')
print(df)
# Filter out non-human devices
#df = df[df['vlan_role'].str.contains('Staff|Faculty|Student')]

# Maximum-in-building filter to remove non-human devices
#df = df[df.groupby('user')['Datetime'].diff().fillna(pd.Timedelta(seconds=0)) < pd.Timedelta(hours=12)]

# Dynamic stay-time filter based on lookup table (in minutes)
mobility_thresholds = {
    (1, 'student'): 5,
    (1, 'staff'): 15,
    (1, 'faculty'): 5,
    (2, 'student'): 5,
    (2, 'staff'): 15,
    (2, 'faculty'): 5,
    (3, 'student'): 10,
    (3, 'staff'): 15,
    (3, 'faculty'): 5,
    (4, 'student'): 10,
    (4, 'staff'): 10,
    (4, 'faculty'): 5,
    (5, 'student'): 15,
    (5, 'staff'): 5,
    (5, 'faculty'): 15,
    (6, 'student'): 15,
    (6, 'staff'): 5,
    (6, 'faculty'): 15,
    (7, 'student'): 10,
    (7, 'staff'): 10,
    (7, 'faculty'): 10,
}
df['mobility_threshold'] = df.apply(lambda x: mobility_thresholds.get((x['Floor'], x['vlan_role']), 15), axis=1)
df['time_in_building'] = df.groupby('user')['Datetime'].diff().fillna(pd.Timedelta(seconds=0)).dt.total_seconds() / 60

# Filter out records with gaps of over 30 minutes between them
df['record_gap'] = df.groupby('user')['Datetime'].diff().fillna(pd.Timedelta(seconds=0)).dt.total_seconds() / 60
df['record_gap'] = df.groupby(['user', 'Floor'])['record_gap'].transform(lambda x: x.cumsum().shift().fillna(0))
df = df[(df['record_gap'] <= 30) | (df['time_in_building'] < df['mobility_threshold'])]

# Print filtered data
print(df)