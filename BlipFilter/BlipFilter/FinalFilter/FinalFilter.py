

# Define function to correct Floor column with variable thresholds
def correct_floor_time_threshold(df, threshold_time_on_initial_floor, threshold_time_on_succeeding_floor):
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
            # Check if previous floor was correct (change of less than threshold_time_on_succeeding_floor minutes and occupancy of at least threshold_time_on_initial_floor minutes on the floor)
            if (row['Datetime'] - last_floor_time).seconds / 60 < threshold_time_on_succeeding_floor and time_on_current_floor >= threshold_time_on_initial_floor:
                # Set corrected floor to previous floor
                corrected_floor.append(last_floor)
                floor = last_floor
            else:
                # Set corrected floor to current floor
                corrected_floor.append(laptoprow['Floor'])
                floor = row['Floor']
                last_floor_time = row['Datetime']
                time_on_current_floor = 0
        else:
            # Set corrected floor to current floor
            corrected_floor.append(row['Floor'])
            last_floor = row['Floor']
            time_on_current_floor += (row['Datetime'] - last_floor_time).seconds / 60
            last_floor_time = row['Datetime']

    # Create a new DataFrame with the same index as the input DataFrame and the corrected_floor as a column
    corrected_floor_df = df.copy()
    corrected_floor_df['Corrected_Floor'] = corrected_floor
    return corrected_floor_df

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