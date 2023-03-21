import pandas as pd
import numpy as np
from scipy.signal import medfilt

# assume your data is stored in a DataFrame called df
# with columns 'datetime', 'user', 'floor'
# Define the path to the data file
path = r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData'

# Load the data into a pandas DataFrame
df = pd.read_csv(path + r'\alk_data_23_02_21Subset.csv')

# Convert to Datetime format
df['Datetime'] = pd.to_datetime(df['Datetime'])

# group data by user
grouped = df.groupby('user')

# apply median filter to each user's floor data
df['filtered_floor'] = grouped['Floor'].apply(lambda x: medfilt(x, kernel_size=3))

# drop the original 'floor' column
df.drop('Floor', axis=1, inplace=True)

# rename the 'filtered_floor' column to 'floor'
df.rename(columns={'filtered_floor': 'Floor'}, inplace=True)

# Save the corrected data to a new file
df.to_csv(path + r'\output\BlipFilter\alk_data_23_02_21-BlipFilterCluster.csv', index=False)