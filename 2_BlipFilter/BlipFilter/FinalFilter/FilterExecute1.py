import pandas as pd

# Load data into a Pandas DataFrame
path = r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData\output'
file = path + "\Preprocessed.alk_data_23_02_19_to_23_04_03.csv"
df = pd.read_csv(file, parse_dates=['Datetime'])

# Convert Datetime column to datetime object
df['Datetime'] = pd.to_datetime(df['Datetime'])

# Sort DataFrame by 'user' and 'Datetime'
df.sort_values(by=['user', 'Datetime'], inplace=True)

# Drop duplicates and unnecessary data
#df = df.drop(columns=['action', 'mac_address'])
df = df.drop_duplicates()

# Group data by user
#df = df.groupby(['user'])


def process_users(df, threshold_time_on_initial_floor=1, threshold_time_on_succeeding_floor=1):
    df['Corrected_Floor'] = df['Floor']
    users = df['user'].unique()

    for user in users:
        user_df = df[df['user'] == user]
        corrected_floor = []

        floor = None
        last_floor = None
        last_floor_time = None
        time_on_current_floor = 0

        for i, row in user_df.iterrows():
            if row['Floor'] != floor:
                if last_floor_time is not None and (row['Datetime'] - last_floor_time).seconds / 60 < threshold_time_on_succeeding_floor and time_on_current_floor >= threshold_time_on_initial_floor:
                    corrected_floor.append(last_floor)
                    floor = last_floor
                else:
                    corrected_floor.append(row['Floor'])
                    floor = row['Floor']
                    last_floor_time = row['Datetime']
                    time_on_current_floor = 0
            else:
                corrected_floor.append(row['Floor'])
                last_floor = row['Floor']
                time_on_current_floor += (row['Datetime'] - last_floor_time).seconds / 60
                last_floor_time = row['Datetime']

            df.at[i, 'Corrected_Floor'] = corrected_floor[-1]

    return df

def correct_isolated_floor_changes(df):
    df['Corrected_Floor'] = df['Floor']
    users = df['user'].unique()

    for user in users:
        user_df = df[df['user'] == user]
        user_df_indices = user_df.index

        for index in range(1, len(user_df_indices) - 1):
            prev_index = user_df_indices[index - 1]
            curr_index = user_df_indices[index]
            next_index = user_df_indices[index + 1]

            prev_floor = df.at[prev_index, 'Corrected_Floor']
            curr_floor = df.at[curr_index, 'Corrected_Floor']
            next_floor = df.at[next_index, 'Corrected_Floor']

            # Condition 2: Check if current floor is different from both previous and next floors
            if curr_floor != prev_floor and curr_floor != next_floor:
                df.at[curr_index, 'Corrected_Floor'] = prev_floor

    return df

# Apply filters
df = process_users(df)
df = correct_isolated_floor_changes(df)

print(df)
df.to_csv(path + "\Filtered.alk_data_23_02_19_to_23_04_03.csv")