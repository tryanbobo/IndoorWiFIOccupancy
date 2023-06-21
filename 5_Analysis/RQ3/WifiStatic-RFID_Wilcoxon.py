
import pandas as pd
from scipy.stats import wilcoxon
import matplotlib.pyplot as plt
# Load the datasets
path_wifi = r"C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData\output\agg\aggDuration"
wifi_data = pd.read_csv(path_wifi + '\BuildingCounts_60min_static.csv')
path_rfid = r"C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\AlkekSensourceData\Final"
rfid_data = pd.read_csv(path_rfid + '\Sensource_2023-02-18--2023-03-04.csv', delimiter=',')
#print(rfid_data.head())
# Convert Datetime column to datetime object and remove timezone information
wifi_data['Datetime'] = pd.to_datetime(wifi_data['Datetime']).dt.tz_convert('US/Central').dt.tz_localize(None)

# Convert RFIDdata datetime column to datetime object
rfid_data['Datetime'] = pd.to_datetime(rfid_data['Datetime'], format='%m/%d/%y %I:%M %p')
#print(rfid_data.head())
# Rename columns in rfid_data for easier merging
rfid_data.columns = ['Location', 'Datetime', 'Ins', 'Outs']

#print(rfid_data.head())
# Merge the two datasets on the Datetime column
merged_data = pd.merge(wifi_data, rfid_data, on='Datetime')
# Remove rows where Total or Ins != 0
merged_data = merged_data.query("Total != 0 and Ins != 0")

merged_data.to_csv(r"C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\Analysis\RQ3_wifi-rfid\RQ3_wifiStatic-rfid.csv")
print(merged_data)
# Extract the columns of interest: 'Total' from wifi_data and 'Ins' from rfid_data
total_wifi = merged_data['Total']
ins_rfid = merged_data['Ins']

# Perform Wilcoxon test
stat, p_value = wilcoxon(total_wifi, ins_rfid)

if p_value <= 0.5:
    print(f"Wilcoxon Test Statistic: {stat}\nP-value: {p_value} \nThe difference between the RFID and Static counts is significant."
          f"\nThe null hypothesis is rejected.")
else:
    print(f"Wilcoxon Test Statistic: {stat}\nP-value: {p_value} \nThe difference between the RFID and Static counts is not significant."
          f"\nThe null hypothesis accepted.")

##########################Plotting#############################

# Set up the plot
plt.figure(figsize=(12, 6))

# Plot the 'Total' field from the wifi data
plt.plot(merged_data['Datetime'], merged_data['Total'], label='Total (Wifi)', marker='o', markersize=4)

# Plot the 'Ins' field from the RFID dataset
plt.plot(merged_data['Datetime'], merged_data['Ins'], label='Ins (RFID)', marker='o', markersize=4)

# Customize the plot
plt.xlabel('Datetime')
plt.ylabel('Count')
plt.title('Comparison of Static Wi-Fi Counts and RFID "In" Count')
plt.legend()
plt.grid()

# Display the plot
plt.show()