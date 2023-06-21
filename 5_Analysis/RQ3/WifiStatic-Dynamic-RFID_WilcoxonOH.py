import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to determine if given time is within operating hours
def within_hours(dt):
    weekday_open, weekday_close = 6.5, 25  # Monday to Thursday, 6:30 am to 1 am next day
    friday_open, friday_close = 6.5, 20  # Friday, 6:30 am to 8 pm
    saturday_open, saturday_close = 9, 19  # Saturday, 9 am to 7 pm
    sunday_open, sunday_close = 9, 25  # Sunday, 9 am to 1 am next day

    if dt.dayofweek == 0:  # Monday
        return weekday_open <= dt.hour < weekday_close
    elif dt.dayofweek == 1:  # Tuesday
        return weekday_open <= dt.hour < weekday_close
    elif dt.dayofweek == 2:  # Wednesday
        return weekday_open <= dt.hour < weekday_close
    elif dt.dayofweek == 3:  # Thursday
        return weekday_open <= dt.hour < weekday_close
    elif dt.dayofweek == 4:  # Friday
        return friday_open <= dt.hour < friday_close
    elif dt.dayofweek == 5:  # Saturday
        return saturday_open <= dt.hour < saturday_close
    else:  # dt.dayofweek == 6, Sunday
        return sunday_open <= dt.hour < sunday_close

# Load the datasets
path_wifi_static = r"C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData\output\agg\aggDuration"
path_wifi_dynamic = r"C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData\output\agg\aggDuration"
path_rfid = r"C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\AlkekSensourceData\Final"

# Load static wifi data
wifi_static_data = pd.read_csv(path_wifi_static + '\BuildingCounts_60min_static.csv')
# Convert Datetime column to datetime object and remove timezone information
wifi_static_data['Datetime'] = pd.to_datetime(wifi_static_data['Datetime']).dt.tz_convert('US/Central').dt.tz_localize(None)
# Filter data according to the opening hours
wifi_static_data = wifi_static_data[wifi_static_data['Datetime'].apply(within_hours)]

# Load dynamic wifi data
wifi_dynamic_data = pd.read_csv(path_wifi_dynamic + '\BuildingCounts_60min_dynamic.csv')
# Convert Datetime column to datetime object and remove timezone information
wifi_dynamic_data['Datetime'] = pd.to_datetime(wifi_dynamic_data['Datetime']).dt.tz_convert('US/Central').dt.tz_localize(None)
# Filter data according to the opening hours
wifi_dynamic_data = wifi_dynamic_data[wifi_dynamic_data['Datetime'].apply(within_hours)]

# Load RFID data
rfid_data = pd.read_csv(path_rfid + '\Sensource_2023-02-18--2023-03-04.csv', delimiter=',')
# Convert RFID data datetime column to datetime object
rfid_data['Datetime'] = pd.to_datetime(rfid_data['Datetime'], format='%m/%d/%y %I:%M %p')
# Filter RFID data according to the opening hours
rfid_data = rfid_data[rfid_data['Datetime'].apply(within_hours)]

# Plotting
plt.rcParams['font.family'] = 'Times New Roman'

fig, ax = plt.subplots(figsize=(12, 6))

# Rename columns in the static and dynamic datasets
wifi_static_data = wifi_static_data.rename(columns={'Total': 'StaticTotal'})
wifi_dynamic_data = wifi_dynamic_data.rename(columns={'Total': 'DynamicTotal'})

# Merge the datasets based on the "Datetime" column
merged_data = pd.merge(wifi_static_data, wifi_dynamic_data, on='Datetime')
merged_data = pd.merge(merged_data, rfid_data, left_on='Datetime', right_on='Datetime')

# Plot the lineplot with the renamed columns
sns.lineplot(x='Datetime', y='StaticTotal', data=merged_data, ax=ax, label='Static WiFi Count', markersize=4)
sns.lineplot(x='Datetime', y='DynamicTotal', data=merged_data, ax=ax, label='Dynamic WiFi Count', markersize=4)
sns.lineplot(x='Datetime', y='Ins', data=merged_data, ax=ax, label='RFID In Counts', markersize=4)

# Set x-axis tick positions for every 2 days
xtick_positions = pd.date_range(start=merged_data['Datetime'].min(), end=merged_data['Datetime'].max(), freq='2D')
# Set x-axis tick labels for the date in the format "YYYY-MM-DD"
xtick_labels = [dt.strftime('%Y-%m-%d') for dt in xtick_positions]
# Set modified x-axis tick positions and labels
ax.set_xticks(xtick_positions)
ax.set_xticklabels(xtick_labels, fontsize=10, rotation=45)

# Set grid lines
ax.grid(True)

# Set x-axis label
ax.set_xlabel('Datetime', fontsize=12)
# Set y-axis label
ax.set_ylabel('Count', fontsize=12)
# Set plot title
ax.set_title('Comparison of Static WiFi, Dynamic WiFi, and RFID "Ins"', fontsize=14)
# set legend on top-right
ax.legend(loc="upper right")
# Display the plot
plt.show()