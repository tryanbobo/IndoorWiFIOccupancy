import pandas as pd
from FinalFilter import correct_floor_time_threshold
from FinalFilter import correct_isolated_floor_changes

# Show full columns at print
pd.set_option('display.max_colwidth', None)
# Load data into a Pandas DataFrame
path = r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData\output'
df = pd.read_csv(path + "\Preprocessed.alk_data_23_02_19_to_23_04_03.csv")

# Convert Datetime column to datetime type
df['Datetime'] = pd.to_datetime(df['Datetime'])

# Sort by Datetime
df.sort_values(by=['user','Datetime'], inplace=True)

## Calculate time difference between consecutive records for each user and floor
#df['time_diff'] = df.groupby(['user', 'Floor'])['Datetime'].diff()
#
## Assign visit IDs
#df['visit_id'] = (df['time_diff'] > pd.Timedelta(hours=1)).cumsum()
#
## Calculate the stay time for each user on each floor per visit
#df['stay_time'] = df.groupby(['user', 'Floor', 'visit_id'])['time_diff'].cumsum()
#
## Group data by user, Floor, and visit_id
#grouped =  df.groupby(['user', 'Floor', 'visit_id'], as_index=False)
# Group data by user
grouped = df.groupby(['user'])

# Call first condition with a 1:1 threshold
corrected_floor_dfs = [correct_floor_time_threshold(group, 1, 1) for _, group in grouped]
df_combined = pd.concat(corrected_floor_dfs)
df_combined = correct_isolated_floor_changes(df_combined)

# Export to csv
df_combined.to_csv(path + "\Filtered.alk_data_23_02_19_to_23_04_03.csv")