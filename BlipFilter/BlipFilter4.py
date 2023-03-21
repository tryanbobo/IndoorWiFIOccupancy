import pandas as pd

# Define the path to the data file
path = r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData'

# Load the data into a pandas DataFrame
df = pd.read_csv(path + r'\alk_data_23_02_21Subset.csv')

# Convert to Datetime format
df['Datetime'] = pd.to_datetime(df['Datetime'])

# Sort the data by user and Datetime
df = df.sort_values(by=['user', 'Datetime'])

# Define a threshold for temporary floor changes
threshold = pd.Timedelta(seconds=30)

# Loop through the records for each user
for user, user_df in df.groupby('user'):

    # Use the floor and time of the first appearance as the starting point for the current floor and current floor start time
    current_floor = user_df['Floor'].iloc[0]
    current_floor_start_time = user_df['Datetime'].iloc[0]

    # Loop through the records for the user
    for i, row in user_df.iterrows():

        # If the user has switched to a new floor
        if row['Floor'] != current_floor:

            # Check if the time spent on the current floor is less than the threshold
            time_on_floor = row['Datetime'] - current_floor_start_time

            if time_on_floor < threshold:
                # Assume that this was a temporary blip and correct the Floor designation
                df.at[i, 'Floor'] = current_floor

            # Update the current floor and start time
            current_floor = row['Floor']
            current_floor_start_time = row['Datetime']

# Save the corrected data to a new file
df.to_csv(path + r'\output\BlipFilter\alk_data_23_02_21-BlipFilter30.csv', index=False)