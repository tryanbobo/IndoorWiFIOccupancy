import pandas as pd

# Load the data

path = r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData\output'
df = pd.read_csv(path + r'\Preprocessed.alk_data_23_02_19_to_23_04_03.csv')
pd.set_option('display.max_columns', None)



# Extract the floor number from the AP name
df['Floor'] = df['AP_Name'].str.extract('(\d+)').astype(int)

# Create a new column 'occupancy_floor' to hold the count of users in each floor at 30 minute intervals
# First, round the Datetime column to the nearest 30 minutes
df['Datetime'] = pd.to_datetime(df['Datetime'])
df['Datetime'] = df['Datetime'].dt.round('30min')

# Next, group by floor and Datetime, and count the unique users in each group
df['occupancy_floor'] = df.groupby(['Floor', pd.Grouper(key='Datetime', freq='30min')])['user'].transform(lambda x: x.nunique())

# Finally, drop duplicates to get a unique count of users in each floor at 30 minute intervals
df_occupancy = df[['Floor', 'Datetime', 'occupancy_floor']].drop_duplicates()

# Print the resulting DataFrame
print(df_occupancy)

df.to_csv(path + r'\BlipFilter\BlipFilter1.csv')