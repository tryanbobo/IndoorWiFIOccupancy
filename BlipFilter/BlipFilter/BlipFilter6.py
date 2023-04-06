import pandas as pd
from io import StringIO
from datetime import timedelta

path = r"C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\spring2023\NeuroNet\output"
file = path + '\GtMerged.csv'
df = pd.read_csv(file, parse_dates=['Datetime'])

# convert Datetime column to datetime type
df['Datetime'] = pd.to_datetime(df['Datetime'])

df.sort_values(['user', 'Datetime'], inplace=True)


def correct_floor(user_data):
    user_data['Corrected_Floor'] = user_data['Floor']

    for i in range(1, len(user_data) - 1):
        prev_floor = user_data.iloc[i - 1]['Floor']
        current_floor = user_data.iloc[i]['Floor']
        next_floor = user_data.iloc[i + 1]['Floor']

        current_time = user_data.iloc[i]['Datetime']
        next_time = user_data.iloc[i + 1]['Datetime']

        # Condition 1
        if prev_floor == next_floor and (next_time - current_time).seconds < 60:
            user_data.at[user_data.index[i], 'Corrected_Floor'] = prev_floor

        # Condition 2
        if i == 1 and prev_floor != current_floor and current_floor != next_floor:
            user_data.at[user_data.index[i], 'Corrected_Floor'] = prev_floor

    return user_data

corrected_floors = df.groupby('user').apply(lambda x: correct_floor(x)).reset_index(drop=True)
corrected_floors = corrected_floors[['Corrected_Floor']]

df = pd.concat([df, corrected_floors], axis=1)

print(df)

df.to_csv(r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\spring2023\BlipFilter\output\BlipFilter6.csv')
