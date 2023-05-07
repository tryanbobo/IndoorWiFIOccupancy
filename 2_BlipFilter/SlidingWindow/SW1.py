import pandas as pd
from scipy import stats
import numpy as np

def rolling_mode(data, window):
    mode_results = []
    for i in range(len(data) - window + 1):
        window_data = data[i:i+window]
        mode_result = stats.mode(window_data, keepdims=False)
        if np.isscalar(mode_result.mode):
            mode = mode_result.mode
        else:
            mode = mode_result.mode[0]
        mode_results.append(mode)
    return mode_results

# Replace the file path with the path to your CSV file
path = r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\spring2023\NeuroNet\output'
file = path + r'\GtMerged.csv'
# Read the CSV file into a DataFrame
df = pd.read_csv(file)

# Define the window size for the rolling mode
window_size = 10
df.sort_values(by=['user', 'Datetime'], inplace=True)
# Calculate the rolling mode of the GroundTruthFloor column
rolling_modes = rolling_mode(df['Floor'].to_numpy(), window_size)

# Print the result
print("Rolling mode of GroundTruthFloor with window size {}: {}".format(window_size, rolling_modes))

# Export to CSV
df.to_csv(path + r'\SW1_out.csv')