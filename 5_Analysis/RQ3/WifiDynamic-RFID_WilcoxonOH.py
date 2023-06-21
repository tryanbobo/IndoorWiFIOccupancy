import pandas as pd
from scipy.stats import wilcoxon, spearmanr
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
path_wifi = r"C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData\output\agg\aggDuration"
wifi_data = pd.read_csv(path_wifi + '\BuildingCounts_60min_dynamic.csv')
path_rfid = r"C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\AlkekSensourceData\Final"
rfid_data = pd.read_csv(path_rfid + '\Sensource_2023-02-18--2023-03-04.csv', delimiter=',')

# Convert Datetime column to datetime object and remove timezone information
wifi_data['Datetime'] = pd.to_datetime(wifi_data['Datetime']).dt.tz_convert('US/Central').dt.tz_localize(None)

# Filter data according to the opening hours
wifi_data = wifi_data[wifi_data['Datetime'].apply(within_hours)]

# Convert RFIDdata datetime column to datetime object
rfid_data['Datetime'] = pd.to_datetime(rfid_data['Datetime'], format='%m/%d/%y %I:%M %p')

# Filter data according to the opening hours
rfid_data = rfid_data[rfid_data['Datetime'].apply(within_hours)]

# Rename columns in rfid_data for easier merging
rfid_data.columns = ['Location', 'Datetime', 'Ins', 'Outs']

# Merge the two datasets on the Datetime column
merged_data = pd.merge(wifi_data, rfid_data, on='Datetime')

# Remove rows where Total or Ins != 0
#merged_data = merged_data.query("Total != 0 and Ins != 0")

merged_data.to_csv(r"C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\Analysis\RQ3_wifi-rfid\RQ3_wifiDynamic-rfid.csv")

# Extract the columns of interest: 'Total' from wifi_data and 'Ins' from rfid_data
total_wifi = merged_data['Total']
ins_rfid = merged_data['Ins']

# Perform Wilcoxon test
stat, p_value = wilcoxon(total_wifi, ins_rfid)

if p_value <= 0.5:
    print(f"Wilcoxon Test Statistic: {stat}\nP-value: {p_value} \nThe difference between the RFID and Dynamic counts is significant."
          f"\nThe null hypothesis is rejected.")
else:
    print(f"Wilcoxon Test Statistic: {stat}\nP-valuef: \nThe difference between the RFID and Dynamic counts is not significant."
    f"\nThe null hypothesis accepted.")

# Perform Spearman's Correlation
correlation, correlation_p_value = spearmanr(total_wifi, ins_rfid)

print(f"Spearman's correlations: {correlation}\nP-value: {correlation_p_value}")

##########################Plotting#############################
# Set font family to Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'

# Set up the plot
plt.figure(figsize=(12, 6))

# Plot the 'Total' field from the wifi data
plt.plot(merged_data['Datetime'], merged_data['Total'], label='Total (Wifi)', marker='o', markersize=4)

# Plot the 'Ins' field from the RFID dataset
plt.plot(merged_data['Datetime'], merged_data['Ins'], label='Ins (RFID)', marker='o', markersize=4)

# Customize the plot
plt.xlabel('Datetime', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.title('Comparison of Dynamic Wi-Fi Counts and RFID "In" Count', fontsize=14)
plt.legend()
plt.grid()

# Display the plot
plt.show()

# Create a scatter plot with a line of best fit.
sns.lmplot(x='Total', y='Ins', data=merged_data, line_kws={'color': 'red'})

# Customize the plot
plt.xlabel('Total Wi-Fi Count', fontsize=12)
plt.ylabel('Total RFID "In" Count', fontsize=12)
plt.title('Correlation between Dynamic Wi-Fi Counts and RFID "In" Count', fontsize=14)

# Display the plot
plt.show()

# Create a scatter plot with a non-linear line of best fit
sns.jointplot(x='Total', y='Ins', data=merged_data, kind='reg', joint_kws={'line_kws':{'color':'red'}})
plt.xlabel('Total Wi-Fi Count', fontsize=12)
plt.ylabel('Total RFID "In" Count', fontsize=12)
plt.title('Correlation between Dynamic Wi-Fi Counts and RFID "In" Count', fontsize=14)

# Display the plot
plt.show()