import pandas as pd
import glob
import os

# List all the CSV files in your directory
path = r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\AlkekSensourceData\Focused'  # Replace with the directory containing your CSV files

all_files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.csv')]

li = []

for filename in all_files:
    try:
        df = pd.read_csv(filename, index_col=None, header=0, encoding='ISO-8859-1', error_bad_lines=False)
    except UnicodeDecodeError:
        df = pd.read_csv(filename, index_col=None, header=0, error_bad_lines=False)
    # Add your code here to delete the 2nd and 75th rows and the 1st column if needed
    li.append(df)

combined_df = pd.concat(li, axis=0, ignore_index=True)
combined_df.to_csv('combined_data.csv', index=False, encoding='utf-8-sig')

print("DataFrames in list:", len(li))

