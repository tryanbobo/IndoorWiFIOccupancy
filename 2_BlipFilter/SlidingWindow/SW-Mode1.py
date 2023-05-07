import pandas as pd
import numpy as np
from scipy import stats

def rolling_mode(data, window):
    mode_results = []
    padded_data = np.pad(data, (window // 2, window // 2), mode='edge')

    for i in range(len(data)):
        window_data = padded_data[i:i + window]
        mode = stats.mode(window_data).mode[0]
        mode_results.append(mode)

    return mode_results

def process_user_data(user_data, window_size):
    user_data = user_data.sort_values(by=['Datetime'])
    user_data['CorrectedFloor'] = rolling_mode(user_data['Floor'].to_numpy(), window_size)
    return user_data

# Read the data
path = r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\spring2023\NeuroNet\output'
file = path + r'\GtMerged.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(file)
# Sort by user and datetime
df = df.sort_values(by=['user', 'Datetime'])

# Group the data by user
grouped_users = df.groupby('user')

window_size = 5
result = []

for user, user_data in grouped_users:
    processed_data = process_user_data(user_data, window_size)
    result.append(processed_data)

# Concatenate the results
processed_df = pd.concat(result)

# Save the processed data
# Replace the file path with the path to your CSV file
path = r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\spring2023\NeuroNet\output'
file = path + r'\GtMerged.csv'
# Read the CSV file into a DataFrame
processed_df.to_csv(path + r'\SW1-Mode_out.csv', index=False)
