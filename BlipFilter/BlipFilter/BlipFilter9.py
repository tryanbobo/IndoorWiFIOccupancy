import pandas as pd

####################
'''
This script is essentially working, except for how the corrected_floor data is being integrated back into the df.
'''
####################

# Load data
path = r"C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\spring2023\NeuroNet\output"
file = path + '\GtMerged.csv'
df = pd.read_csv(file, parse_dates=['Datetime'])

# Convert Datetime column to datetime object
df['Datetime'] = pd.to_datetime(df['Datetime'])

# Sort DataFrame by 'user' and 'Datetime'
df.sort_values(by=['user', 'Datetime'], inplace=True)

# Group data by user
grouped = df.groupby(['user'])

# Define function to correct Floor column
def correct_floor(df):
    # Initialize variables
    floor = df.iloc[0]['Floor']
    last_floor = floor
    last_floor_time = df.iloc[0]['Datetime']
    time_on_current_floor = 0
    corrected_floor = []

    # Iterate through rows in the DataFrame
    for i, row in df.iterrows():
        # Condition 1: Check if floor has changed
        if row['Floor'] != floor:
            # Check if previous floor was correct (change of less than 2 minutes and occupancy of at least 3 minutes on the floor)
            if (row['Datetime'] - last_floor_time).seconds / 60 < 2 and time_on_current_floor >= 3:
                # Set corrected floor to previous floor
                corrected_floor.append(last_floor)
                floor = last_floor
            else:
                # Set corrected floor to current floor
                corrected_floor.append(row['Floor'])
                floor = row['Floor']
                last_floor_time = row['Datetime']
                time_on_current_floor = 0
        else:
            # Set corrected floor to current floor
            corrected_floor.append(row['Floor'])
            last_floor = row['Floor']
            time_on_current_floor += (row['Datetime'] - last_floor_time).seconds / 60
            last_floor_time = row['Datetime']

    return corrected_floor

# Create Corrected_Floor column
df['Corrected_Floor'] = grouped.apply(correct_floor).reset_index(level=0, drop=True)

# Define function to correct isolated floor changes (Condition 2)
def correct_isolated_floor_changes(df):
    for index in range(1, len(df) - 1):
        prev_floor = df.at[index - 1, 'Corrected_Floor']
        curr_floor = df.at[index, 'Corrected_Floor']
        next_floor = df.at[index + 1, 'Corrected_Floor']

        # Condition 2: Check if current floor is different from both previous and next floors
        if curr_floor != prev_floor and curr_floor != next_floor:
            df.at[index, 'Corrected_Floor'] = prev_floor

    return df

# Apply the function to correct isolated floor changes
df = df.groupby(['user']).apply(correct_isolated_floor_changes)

# Save corrected data
df.to_csv(r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\spring2023\BlipFilter\output\BlipFilter9.csv')