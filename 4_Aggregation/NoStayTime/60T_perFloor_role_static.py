import matplotlib.pyplot as plt
import pandas as pd
import os

# Read the CSV file
path = r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData\output'
filtered_data = pd.read_csv(os.path.join(path, 'Mobility(Static)_Non-humanFilter.csv'))

# Convert Datetime column to datetime type and round to 60-minute intervals
filtered_data['Datetime'] = pd.to_datetime(filtered_data['Datetime']).dt.round('60min')

# Create a DataFrame with all possible combinations of Datetime and Corrected_Floor
unique_datetimes = filtered_data['Datetime'].unique()
unique_floors = filtered_data['Corrected_Floor'].unique()

all_combinations = pd.MultiIndex.from_product([unique_datetimes, unique_floors], names=['Datetime', 'Corrected_Floor']).to_frame(index=False)

# Group the filtered_data by Datetime and Corrected_Floor, and count the number of records for each vlan_role
grouped_data = filtered_data.groupby(['Datetime', 'Corrected_Floor', 'vlan_role']).size().reset_index(name='count')

# Pivot the grouped_data to have columns for each vlan_role
pivoted_data = grouped_data.pivot_table(values='count', index=['Datetime', 'Corrected_Floor'], columns='vlan_role', fill_value=0).reset_index()

# Merge all_combinations with pivoted_data to ensure every floor is represented at each 60-minute interval
merged_data = all_combinations.merge(pivoted_data, on=['Datetime', 'Corrected_Floor'], how='left').fillna(0)

# Calculate the total count for each row and reorder the columns
merged_data['Total'] = merged_data['Guest'] + merged_data['Staff'] + merged_data['Student']
merged_data = merged_data[['Datetime', 'Corrected_Floor', 'Guest', 'Staff', 'Student', 'Total']]

# Sort the DataFrame by 'Datetime' and 'Corrected_Floor'
merged_data = merged_data.sort_values(['Datetime', 'Corrected_Floor'])

# Save the DataFrame to a CSV file
merged_data.to_csv(os.path.join(path, 'agg\FloorCounts_60min_Static.csv'), index=False)

############Plotting################
# Sort the unique_floors list
unique_floors = sorted(unique_floors)

# Create a plot
fig, ax = plt.subplots(figsize=(15, 6))
for floor in unique_floors:
    floor_data = merged_data[merged_data['Corrected_Floor'] == floor]
    ax.plot(floor_data['Datetime'], floor_data['Total'], label=f'Floor {floor}')

# Format the x-axis
ax.set_xlabel('Datetime')
ax.xaxis.set_major_locator(plt.MaxNLocator(20))
plt.xticks(rotation=45)

# Format the y-axis
ax.set_ylabel('Total Count')

# Add a legend and title
ax.legend()
ax.set_title('Counts of Every Floor at Every 1-hour Interval: Static Filter')

# Show the plot
plt.tight_layout()
plt.show()