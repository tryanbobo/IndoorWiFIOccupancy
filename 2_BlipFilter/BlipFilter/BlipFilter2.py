import pandas as pd


path = r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData'
# Load the data into a pandas DataFrame
df = pd.read_csv(path + r'\alk_data_23_02_21Subset.csv')
# Convert to Datatime format
df['Datetime'] = pd.to_datetime(df['Datetime'])
# Sort the data by user and Datetime
df = df.sort_values(by=['user', 'Datetime'])

# Define a threshold for temporary floor changes
threshold = pd.Timedelta(minutes=1)

# Initialize variables for tracking the current floor and time spent on each floor
current_floor = df['Floor'].iloc[0]
current_floor_start_time = df['Datetime'].iloc[0]
changed_records = []

# Loop through the records for each user
for i, row in df.iterrows():
    # If the user has switched to a new floor
    if row['Floor'] != current_floor:
        # Check if the time spent on the current floor is less than the threshold
        time_on_floor = row['Datetime'] - current_floor_start_time
        if time_on_floor < threshold:
            # Assume that this was a temporary blip and correct the Floor designation
            df.at[i, 'Floor'] = current_floor
            changed_records.append(i)
        else:
            # Update the current floor and start time
            current_floor = row['Floor']
            current_floor_start_time = row['Datetime']
    else:
        # Update the current floor start time
        current_floor_start_time = row['Datetime']

# Add a new column to the data to keep track of the records that were changed
df['changed'] = False
df.at[changed_records, 'changed'] = True

# Save the corrected data to a new file
df.to_csv(path + r'\output\2_BlipFilter\alk_data_23_02_21-2_BlipFilter.csv', index=False)