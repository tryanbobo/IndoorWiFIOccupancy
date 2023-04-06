import pandas as pd

# load data
path = r"C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\spring2023\NeuroNet\output"
file = path + '\GtMerged.csv'
df = pd.read_csv(file, parse_dates=['Datetime'])

# convert Datetime column to datetime object
df['Datetime'] = pd.to_datetime(df['Datetime'])

# sort dataframe by Datetime column
df = df.sort_values(by='Datetime')

# define function to correct Floor column
def correct_floor(df):
    # initialize variables
    floor = 0
    last_floor = 0
    last_floor_time = pd.to_datetime('1900-01-01')
    corrected_floor = []
    for i, row in df.iterrows():
        # check if floor has changed
        if row['Floor'] != floor:
            # check if previous floor was correct
            if (row['Datetime'] - last_floor_time).seconds / 60 < 2:
                # set corrected floor to previous floor
                corrected_floor.append(last_floor)
                floor = last_floor
            else:
                # set corrected floor to current floor
                corrected_floor.append(row['Floor'])
                floor = row['Floor']
                last_floor_time = row['Datetime']
        else:
            # set corrected floor to current floor
            corrected_floor.append(row['Floor'])
            last_floor = row['Floor']
            last_floor_time = row['Datetime']
    return corrected_floor

# create corrected floor column
df['Corrected_Floor'] = correct_floor(df)

# define function to correct isolated floor changes
def correct_isolated_floor_changes(df):
    corrected_floor = []
    for i, row in df.iterrows():
        # check if current row has floor 2 surrounded by floor 1s
        if (row['Floor'] == 2 and i > 0 and i < len(df) - 1 and
            df.iloc[i-1]['Floor'] == 1 and df.iloc[i+1]['Floor'] == 1):
            # set corrected floor to 1
            corrected_floor.append(1)
        else:
            # set corrected floor to original floor
            corrected_floor.append(row['Corrected_Floor'])
    return corrected_floor

# create final corrected floor column
df['Corrected_Floor'] = correct_isolated_floor_changes(df)

# save corrected data
df.to_csv(r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\spring2023\BlipFilter\output\BlipFilter7.csv')