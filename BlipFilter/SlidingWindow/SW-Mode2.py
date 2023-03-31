import pandas as pd
from scipy.stats import mode
import csv
# Replace the file path with the path to your CSV file
path = r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\spring2023\NeuroNet\output'
file = path + r'\GtMerged.csv'
# Read the CSV file into a DataFrame
df = pd.read_csv(file)

df = df.drop(columns=['Unnamed: 0', 'action', 'mac_address'], axis=1)

df = df.drop_duplicates()

df = df.sort_values(by=['user', 'Datetime'])

df['CorrectedFloor'] = df['Floor'].rolling(window=5).apply(lambda x: mode(x)[0])

print(df)



df.to_csv(path + '\SW-Mode2_out.csv', index=False)

