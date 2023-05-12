import pandas as pd
from scipy.stats import wilcoxon

# Load ground truth data
ground_truth_data = pd.read_csv(r"C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\GroundTruth\GroundTruth-03-02-2023_Simple.csv")
# Convert Median_Time column to datetime type
ground_truth_data['Median_Time'] = pd.to_datetime(ground_truth_data['Median_Time'])

# load Wifi data
# Static
path = r"C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData\output"
filtered_data_static = pd.read_csv(path + r"\Mobility(Static)_Non-humanFilter.csv")

# Convert 'Datetime' column to datetime type and 'stay_time' column to timedelta type
filtered_data_static['Datetime'] = pd.to_datetime(filtered_data_static['Datetime'])
filtered_data_static['Datetime'] = filtered_data_static['Datetime'].dt.tz_convert(None)  # Remove timezone information
filtered_data_static['stay_time'] = pd.to_timedelta(filtered_data_static['stay_time'])

#Define a function to find the WiFi data count for each ground truth record
#find the value between the Datetime and Datetime + stay_time
def find_wifi_data_count(floor, median_time, filtered_data):
    # Filter the filtered_data to match the floor and median_time
    matching_data = filtered_data[
        (filtered_data['Corrected_Floor'] == floor) &
        (filtered_data['Datetime'] <= median_time) &
        (filtered_data['Datetime'] + filtered_data['stay_time'] >= median_time)]

    # Get the number of users from the matching data
    count = matching_data['user'].count()

    return count

ground_truth_data['WiFi_Count_Static'] = ground_truth_data.apply(lambda row: find_wifi_data_count(row['Floor'], row['Median_Time'], filtered_data_static), axis=1)

print(ground_truth_data)

## Calculate the Wilcoxon test
#w, p = wilcoxon(ground_truth_data['MedianTotal'], ground_truth_data['WiFi_Count_Static'])
#
#print(f"Wilcoxon test result: W = {w}, p-value = {p}")

## Define the target floor and time
#target_floor = 3
#target_time = pd.Timestamp("2023-03-02 14:02:00")
#
## Filter the DataFrame for the target floor
#floor_data = filtered_data_static[filtered_data_static['Corrected_Floor'] == target_floor]
#
## Filter the DataFrame for the target time
#matching_data = floor_data[
#    (floor_data['Datetime'] <= target_time) &
#    (floor_data['Datetime'] + floor_data['stay_time'] >= target_time)
#]
#
## Count the number of rows in the matching_data DataFrame
#count = len(matching_data)
#
#print(f"Number of people on the {target_floor}rd floor at {target_time}: {count}")